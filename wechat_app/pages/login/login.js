const app = getApp();

Page({
    data: {
        username: '',
        password: '',
        role:'user'
    },
    bindUsernameInput: function(event) {
        this.setData({
            username: event.detail.value
        });
    },
    bindPasswordInput: function(event) {
        this.setData({
            password: event.detail.value
        });
    },
    bindRoleSelect: function(event) {
        this.setData({
            role: event.detail.value
        });
    },
    login: function() {

        const { username, password ,role } = this.data;
        if (!username || !password) {
            wx.showToast({
                title: '用户名或密码不能为空',
                icon: 'none'
            });
            return;
        }
        wx.request({
            url: 'https://app6321.acapp.acwing.com.cn/user_login/', 
            method: 'GET',
            data: {
                username: username,
                password: password,
                role: role
            },
            success: function(res) {
                if (res.data.status === 'success') {
                    wx.showToast({
                        title: '登录成功',
                        icon: 'success'
                    });
                    
                    wx.setStorageSync('username', username);

                    if (role === 'user') {
                        wx.redirectTo({
                            url: '/pages/user/manage/manage'
                        });
                    }
                    else if (role === 'repair_man'){
                        wx.redirectTo({
                            url: '/pages/repair_man/home/home'
                        });
                    }
                    
                } 
                else {
                    wx.showToast({
                        title: res.data.message,
                        icon: 'none'
                    });
                }
            },
            fail: function() {
                wx.showToast({
                    title: '登录请求失败',
                    icon: 'none'
                });
            }
        });
    }
});
