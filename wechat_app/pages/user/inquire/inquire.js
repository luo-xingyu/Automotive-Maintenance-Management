Page({
    data: {
        username: "",
        entrusts: [], 
    },

    onLoad: function(options) {
        this.username = wx.getStorageSync('username');
        this.fetchEntrusts();
    },

    fetchEntrusts: function() {
        var that = this;
        wx.request({
            url    : 'https://app6321.acapp.acwing.com.cn/user_commission/',
            method : 'GET',
            data   : {
                username: that.username,
            },
            success: function(res) {
                that.setData({
                    entrusts: res.data
                });
            }
        });
    },

    queryProgress: function(e) {
        const entrustId = e.currentTarget.dataset.entrustId;

        wx.request({
            url    : 'https://app6321.acapp.acwing.com.cn/user_progressquery/',
            method : 'GET',
            data   : {
                entrust_id: entrustId
            },
            success: function(res) {
                let content = '';

                res.data.forEach((order, index) => {  
                    content += '委托 ' + (index + 1) + ':\r\n';
                    content += order.project + ' - ' + (order.progress ? '完成' : '未完成') + '\r\n';  
                });

                wx.showModal({
                    title: '委托进度',
                    content: content,
                    showCancel: false
                });
            }
        });
    },

    payForEntrust: function(e) {
        const entrustId = e.currentTarget.dataset.entrustId;
        
        wx.request({
            url    : 'https://app6321.acapp.acwing.com.cn/user_pay/',
            method : 'GET',
            data   : {
                entrust_id: entrustId
            },
            success: function(res) {
                wx.showToast({
                    title: '支付成功',
                    icon : 'success'
                });
            }
        });
    }
});
