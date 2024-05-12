Page({
    data  :{
        userType : 'repairman',
    },
    onLoad: function(options) 
    {
        this.username = wx.getStorageSync('username');
    },
    
    Show:function(options) {
        
    }
});