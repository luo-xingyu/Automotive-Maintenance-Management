Page({
    onShow:function(options) {
        console.log( this.getTabBar() + 'home');
        this.getTabBar().updateTabs(); 
        if (typeof this.getTabBar === 'function' &&
            this.getTabBar()) {
            this.getTabBar().setData({
                selected: 3
            })
        }
    }
});