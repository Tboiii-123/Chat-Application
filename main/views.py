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


User = get_user_model()


# @login_required(login_url='/login/')
# def index(request):


#     user = request.user.profile


#     friends =Friend.objects.exclude(profile=request.user.profile)

#         # last_msg =ChatMessage.objects.all(
#         #     msg_sender=
#         #     msg_receiver
#         # )


#     return render(request,'index.html',{
#         'friends':friends,
#         'user':user
        
#     })


from django.db.models import Q

@login_required(login_url='/login/')
def index(request):
    user = request.user.profile
    friends = Friend.objects.exclude(profile=user)

    friends_with_last_msg = []

    for friend in friends:
        # Get the friend's profile
        friend_profile = friend.profile

        # Get the last message between user and this friend
        last_msg = ChatMessage.objects.filter(
            Q(msg_sender=user, msg_receiver=friend_profile) |
            Q(msg_sender=friend_profile, msg_receiver=user)
        ).order_by('-id').first()

        friends_with_last_msg.append({
    
              "friend_username": friend_profile.username,  # ✅ Username
            "friend_profile": friend_profile,  
            "last_msg": last_msg
        })

    return render(request, 'index.html', {
        'friends_with_last_msg': friends_with_last_msg,
        'user': user,

    })



def register(request):
       
    if request.method =="POST":


        username =request.POST.get('username')


        firstname =request.POST.get('firstname')

        lastname =request.POST.get('lastname')

        email =request.POST.get('email')

        
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
                
        
        email =request.POST.get('email')
        

        user_profile.profile_img =image

        user_profile.save()


    
        return redirect('profile')

     
    return render(request,'profile.html',{
        'profile':user_profile
        
    })


@login_required(login_url='/login/')
def chat(request,pk):

    friend = Friend.objects.get(profile_id=pk)
    sender_profile =request.user.profile


    receiver_profile  =Profile.objects.get(id=friend.profile.id)


    chats =ChatMessage.objects.all()

    recv_message  =ChatMessage.objects.filter(
        msg_sender =receiver_profile,
        msg_receiver =sender_profile
    )
    

    if request.method == "POST":

        Msg=request.POST.get('message')


        ChatMessage.objects.create(
            body =Msg,
            msg_sender=sender_profile,
            msg_receiver=receiver_profile
        )

        

        return redirect('chat',pk=friend.profile.id)


    return render(request,'chat.html',{
        'friend':friend,
        'user':sender_profile,
        'receiver':receiver_profile,
        'chats':chats,
        'num':recv_message.count(),
        
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


def receivedMessages(request,pk):
    friend = Friend.objects.get(profile_id=pk)
    sender_profile =request.user.profile
    receiver_profile  =Profile.objects.get(id=friend.profile.id)
    # Getting all the chat
    chats_arr =[]
    chats =ChatMessage.objects.filter(
        msg_sender =receiver_profile,
        msg_receiver =sender_profile
    )


    for chat in chats:
        chats_arr.append(chat.body)


    return JsonResponse(chats_arr,safe=False)





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









'''
lawalhussein775@gmail.com
123


wakil
tayelawal775@gmail.com
123

fatai
fatailawal@gmail.com
123

raez
raez@gmail.com
123
'''