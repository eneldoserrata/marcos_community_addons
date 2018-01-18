openerp_announcement = function(instance) {
    instance.web.WebClient.include({
        show_application: function() {
            console.log("RrrrrrRR111");
            return 
        },
        _ab_location: function(dbuuid) {
            console.log("RrrrrrRR222");
            return '';
        },
        show_annoucement_bar: function() {
            console.log("RrrrrrRR333");
           
           
        }
    });
};
