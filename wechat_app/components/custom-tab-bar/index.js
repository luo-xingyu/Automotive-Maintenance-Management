// components/custom-tab-bar/index.js
Component({
    data: {
        selected: 0,
        color: "#7A7E83",
        selectedColor: "#3cc51f",
        tabs: [],
        list1: [
            {
            "pagePath": "pages/repair_man/work/work",
            "text": "管理",
            "iconPath": "/static/image/icon/qianshoushenpitongguo-xianxing.png",
            "selectedIconPath": "/static/image/icon/qianshoushenpitongguo.png"
            },

            {
            "pagePath": "pages/repair_man/home/home",
            "text": "我的",
            "iconPath": "/static/image/icon/hezuoguanxi-xianxing.png",
            "selectedIconPath": "/static/image/icon/hezuoguanxi.png"
            }
        ],
        list2: [
            {
                "pagePath": "pages/user/inquire/inquire",
                "text": "查询",
                "iconPath": "/static/image/icon/sousuo-xianxing.png",
                "selectedIconPath": "/static/image/icon/sousuo.png"
            },
            {
                "pagePath": "pages/user/manage/manage",
                "text": "管理",
                "iconPath": "/static/image/icon/danju-xianxing.png",
                "selectedIconPath": "/static/image/icon/danju.png"
            },
            {
                "pagePath": "pages/user/home/home",
                "text": "我的",
                "iconPath": "/static/image/icon/hezuoguanxi-xianxing.png",
                "selectedIconPath": "/static/image/icon/hezuoguanxi.png"
            }
        ]
    },
    attached() {
        this.updateTabs();
    },
    pageLifetimes: {
        show() {
            this.updateTabs();
        }
    },
    methods: {
        switchTab(e) {
            const data = e.currentTarget.dataset
            const url = data.path
            wx.switchTab({url})
            this.setData({
            selected: data.index
            })
        },
        updateTabs() {
            const app = getApp();
            const userType = app.globalData.userType;
            console.log(userType);
            if (userType === 'repairman') {
                this.setData({ tabs: this.data.list1 });
            } else {
                this.setData({ tabs: this.data.list2 });
            }
        }
    }
})