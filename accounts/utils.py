def detectUser(User):
    if User.role == 1:
        redirect_url = 'vendorDashboard'
        return redirect_url
    elif User.role == 2:
       redirect_url = 'custDashboard'
       return redirect_url
    
    elif user.role == None and user.is_superadmin:

        redirect_url = '/admin'
        return redirect_url  
    
