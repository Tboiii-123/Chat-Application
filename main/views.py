from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
#To register we import
from django.contrib.auth import get_user_model
#For pop up messages
from django.contrib import messages
#For Authentification
from django.contrib.auth import authenticate,login ,logout
from .models import Profile,ChatMessage,Friend
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q, Count





User = get_user_model()



def get_friends_with_data(user):
    friends = Friend.objects.exclude(profile=user)
    friends_data = []
    for friend in friends:
        last_msg = ChatMessage.objects.filter(
            Q(msg_sender=user, msg_receiver=friend.profile) |
            Q(msg_sender=friend.profile, msg_receiver=user)
        ).order_by('-id').first()

        unread_count = ChatMessage.objects.filter(
            msg_sender=friend.profile, msg_receiver=user, is_read=False
        ).count()

        friends_data.append({
            "id": friend.profile.id,
            "username": friend.profile.username,
            "profile_img": friend.profile.profile_img.url if friend.profile.profile_img else None,
            "last_msg": last_msg.body if last_msg else "No messages yet",
            "last_msg_time": last_msg.created_at.strftime("%H:%M") if last_msg else "",
            "unread_count": unread_count,
        })
    return friends_data
@login_required(login_url='/login/')
def index(request):
    user = request.user.profile
    friends_with_last_msg = get_friends_with_data(user)
    return render(request, 'index.html', {
        'friends_with_last_msg': friends_with_last_msg,
        'user': user,
    })


@login_required(login_url='/login/')
def friends_list(request):
    user = request.user.profile
    return JsonResponse({"friends": get_friends_with_data(user)})



def register(request):
       
    if request.method =="POST":


        username =request.POST.get('username')


        firstname =request.POST.get('firstname')

        lastname =request.POST.get('lastname')

        email =request.POST.get('email')

        number =request.POST.get('number')

        
        password1 =request.POST.get('password1')

        password2=request.POST.get('password2')
       
        
        if firstname =='' or lastname =='' or username=='' or   password1 =='' or password2 =='':
             
            messages.error(request,("All Entry must be filled......"))
            return redirect('register')

        else:
         
                if User.objects.filter(email=email).exists():

                    messages.error(request,("Sorry!!,there was a problem registering. Username already taken. Please try again...."))

                    return redirect('register')

                elif password1 != password2:
                    messages.error(request,("Sorry!!,Make sure your password matches...."))

                    return redirect('register')
        
                else:
                    try:
                                                
                        user=  User.objects.create_user(email=email,                                                            
                                                            first_name=firstname, 

                                                            last_name =lastname,
                                                            

                                                            password=password1,
                                                            )
                        

                          
                        user_model =User.objects.get(email=email)

                        
                        new_profile =Profile.objects.create(user =user_model,
                                                            
                                                            fname =user_model.first_name,
                                                            email=user_model.email,

                                                            lname =user_model.last_name ,
                                                            number =number,
                                                            username =username                                                        
                                                            )

                
                        new_profile.save()
                
                        

                        messages.success(request,("You Have Regsitered Successfully......."))
                

                        return redirect('login')

                    except Exception as e:
                            messages.error(request, f"An error occurred: {str(e)}. Please try again.")
                            return redirect('register')

    
        




    return render(request,'register.html',{
        
    })




def Login(request):

    
    if request.method =="POST":
        email =request.POST.get("email")
        password =request.POST.get("password")

        user =authenticate(request,email=email , password =password)
        if user is not None:
            login(request,user)
            messages.success(request,'You have been logged in Successfully!!!!!!')

            return redirect('profile')
            
        else:
            messages.error(request,'There was an error when logging in,Please Login in again!!!!!')
            
            return redirect('login')
    


    return render(request,'login.html',{
        
    })

def Logout(request):

    
    logout(request)

    messages.success(request,'Logged out sucessfully.....')


    return redirect('login')

@login_required(login_url='/login/')
def profile(request):

    
    user_profile =Profile.objects.get(user=request.user)

    if request.method == "POST":

        if request.FILES.get('image') == None:
            image =user_profile.profile_img

        else:
            
            image =request.FILES.get('image')
                
        
        username =request.POST.get('username')
        
        number =request.POST.get('number')
        about =request.POST.get('about')

        user_profile.username =username
        user_profile.number =number
        user_profile.about =about
        
        

        user_profile.profile_img =image

        user_profile.save()


    
        return redirect('profile')

     
    return render(request,'profile.html',{
        'profile':user_profile
        
    })


@login_required(login_url='/login/')
def chat(request, pk):
    friend = get_object_or_404(Friend, profile_id=pk)
    sender_profile = request.user.profile
    receiver_profile = friend.profile

    # Get all chat messages between the two
    chats = ChatMessage.objects.filter(
        Q(msg_sender=sender_profile, msg_receiver=receiver_profile) |
        Q(msg_sender=receiver_profile, msg_receiver=sender_profile)
    ).order_by("created_at")  # oldest first

    recv_message_count = ChatMessage.objects.filter(
        msg_sender=receiver_profile,
        msg_receiver=sender_profile
    ).count()

    if request.method == "POST":
        Msg = request.POST.get('message')
        if Msg:
            ChatMessage.objects.create(
                body=Msg,
                msg_sender=sender_profile,
                msg_receiver=receiver_profile
            )
        return redirect('chat', pk=friend.profile.id)

    return render(request, 'chat.html', {
        'friend': friend,
        'user': sender_profile,
        'receiver': receiver_profile,
        'chats': chats,
        'num': recv_message_count,
    })



def sent_msg(request,pk):
    friend = Friend.objects.get(profile_id=pk)
    sender_profile =request.user.profile

    receiver_profile  =Profile.objects.get(id=friend.profile.id)
    
    data =json.loads(request.body)

    new_chat =data['msg']
    new_chat_message =ChatMessage.objects.create(
            body =new_chat,
            msg_sender=sender_profile,
            msg_receiver=receiver_profile,
            is_read =False
        )


    return JsonResponse(new_chat_message.body,safe=False)


from django.http import JsonResponse
from .models import ChatMessage, Friend, Profile

def receivedMessages(request, pk):
    friend = Friend.objects.get(profile_id=pk)
    sender_profile = request.user.profile
    receiver_profile = Profile.objects.get(id=friend.profile.id)

    chats_arr = []

    chats = ChatMessage.objects.filter(
        msg_sender=receiver_profile,
        msg_receiver=sender_profile
    )

    for chat in chats:
        if chat.voice_note:
            # If it's a voice note, send type and URL
            chats_arr.append({
                "type": "voice",
                "url": chat.voice_note.url
            })
        else:
            # Otherwise, send text message
            chats_arr.append({
                "type": "text",
                "content": chat.body
            })

    return JsonResponse(chats_arr, safe=False)






def chatNotification(request):
    friends =Friend.objects.exclude(profile=request.user.profile)


    
    sender_profile =request.user.profile
    arr =[]
    
    

    for friend in friends:
        chats =ChatMessage.objects.filter(
        msg_sender =friend.profile.id,
        msg_receiver =sender_profile,
        is_read = False
    )
        
        
        arr.append(chats.count())

    



    return JsonResponse(arr, safe=False)

def settings(request):
    sender_profile =request.user.profile
    
    


    return render(request,'settings.html',{
        'user':sender_profile

    })



@login_required(login_url='/login/')
def delete_account(request):
    user = request.user
    user.delete()  # This deletes user + linked profile automatically if CASCADE
    return redirect('register')  # Redirect to signup or homepage



@login_required(login_url='/login/')
def friend_detail(request, profile_id):
    friend_profile = get_object_or_404(Profile, id=profile_id)
    context = {
        'friend': friend_profile
    }
    return render(request, 'friend_details.html', context)




@csrf_exempt
def send_voice_note(request, profile_id):
    if request.method == "POST" and request.FILES.get("voice_note"):
        voice = request.FILES["voice_note"]
        chat = ChatMessage.objects.create(
            msg_sender=request.user.profile,
            msg_receiver_id=profile_id,
            voice_note=voice  # make sure your ChatMessage has a voice_note FileField
        )
        return JsonResponse({"url": chat.voice_note.url})
    return JsonResponse({"error": "No voice note"}, status=400)


