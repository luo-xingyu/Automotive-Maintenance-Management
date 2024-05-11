Page({
    data: {
        username: '',
        Types: ['小型车', '微型车', '紧凑车型', '中等车型','高级车型','豪华车型','三厢车型','CDV','MPV','SUV'],  
        selectedType: '',
        vehicles: [],
        isModalOpen: false
    },
    onLoad: function(options) {
        //获取当前用户所有车辆列表 设置给vehicles
        this.setData({
            vehicles: [{type: '轿车', plateNumber: 'ABC123', frameNumber: 'XYZ789'}]
        });
        username = wx.getStorageSync('username');
    },
    openModal: function() {
        this.setData({ isModalOpen: true });
    },
    closeModal: function() {
        this.setData({ isModalOpen: false });
    },
    pickerChange: function(e) {
        this.setData({
            selectedType: this.data.Types[e.detail.value]
        });
    },
    // 处理添加车辆的表单提交
    submitForm: function(e) {

        const { type, license_plate, ident_number } = e.detail.value;
        this.data.vehicles.push({ type, license_plate, ident_number });
        this.setData({
            vehicles: this.data.vehicles
        });

        wx.request({
            url: 'https://app6321.acapp.acwing.com.cn/user_managecar/', 
            method: 'GET',
            data: {
                type: type,
                license_plate: license_plate,
                ident_number
            },
            success: function(res) {
                if (res.data.status === 'success') {
                    wx.showToast({
                        title: '登录成功',
                        icon: 'success'
                    });
            }
        })
    },
    // 删除车辆
    deleteVehicle: function(e) {
       
        const plateNumber = e.currentTarget.dataset.platenumber;
        const vehicles = this.data.vehicles.filter(v => v.plateNumber !== plateNumber);
        this.setData({
            vehicles
        });
        // 向服务器发送删除请求的代码也可以在这里添加

    }
  });
  