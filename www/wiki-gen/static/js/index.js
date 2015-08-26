$(document).ready(function() {
    wikiFunction("docReady") });
$(window).on('resize', function() { 
    wikiFunction("docResize") });

function wikiFunction(status) {
    //Stretches menu to height of page
    $(".menu-off").css("height", $(document).innerHeight());
    
    //Handles menu pop-up
    if (status == "docReady") {
        $("nav").click(function() {
            $(".menu-off").toggleClass("menu-on");
            $(".main-text").toggleClass("main-text-on");
            $(".title").toggleClass("title-on");
            $("header").toggleClass("header-menu-on");
        });
        $("section").click(function() {
            if ($(".menu-off").attr("class") == "menu-off menu-on") {
                $(".menu-off").removeClass("menu-on");
                $(".main-text").removeClass("main-text-on");
                $(".title").removeClass("title-on");
                $("header").removeClass("header-menu-on"); 
            }
        });
        
    }
}
