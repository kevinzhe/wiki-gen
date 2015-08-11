$(document).ready(function() {
    wikiFunction("docReady") });
$(window).on('resize', function() { 
    wikiFunction("docResize") });

function wikiFunction(status) {
    //load title name for each page
    var titleName = $(".title h1").text();
    $("title").text(titleName);
    
    //text input color when focused/unfocused
    $("input").focusin(function () {
        $("input[type='text']").css("color", "rgba(0,0,0,0.9)");
    });
    $("input").focusout(function () {
        $("input[type='text']").css("color", "rgba(0,0,0,0.2)"); 
    });
    
    //placement of section (rest of text)
    $("section").css("top", $("header").css("height"));
    
    //text replacement generator
    var bodyText = $(".main-text").html();
    var articleTitle = $("div h1").text();
    bodyText = bodyText.replace(articleTitle, 
                                "<b>" + articleTitle + "</b>");
    $(".main-text").html(bodyText);
    
    // drop down menu for smaller devices
    $(".navigation-menu a").css("width", parseInt($("header").css("width")));
    
    if ($(window).innerWidth() < 768) {
        $(".navigation-menu img").attr("src", "");
        $(".navigation-menu a").hide();
    }
    else {
        $(".navigation-menu img").attr("src", "img/wikigenLogo.png");
        $(".navigation-menu").css("display", "block");
    }
    
    if ($(window).innerWidth() > 768) {
    //nav bar on left side
    $("nav").css("height", parseInt($("header").css("height")) +
                 parseInt($("section").css("height")));
    }
    else { 
        $("nav").css("height", "100%"); 
    }
    
    if (status == "docReady") { //document ready only
        //for action commands
        $("nav").click(function () {
            if ($(window).innerWidth() < 768) {
                if ($(".navigation-menu a").css("display") == "none") {
                    $(".navigation-menu a").slideDown("1000"); 
                }
                else { $(".navigation-menu a").slideUp("1000");  }
            }
        });
        $("section").click(function () {
            if ($(window).innerWidth() < 768) {
                if ($(".navigation-menu a").css("display") != "none") {
                    $(".navigation-menu a").slideUp("1000");    
                }
            } 
        });
        $(".sections h3").click(function() {
            if ($(this).children(":first").attr("class") == 
                "glyphicon glyphicon-menu-down") {
                $(this).children(":first").removeClass(
                    "glyphicon-menu-down").addClass("glyphicon-menu-up");
                $(this).next().css("display", "block");
            }
            else {
                $(this).children(":first").removeClass(
                    "glyphicon-menu-up").addClass("glyphicon-menu-down");
                $(this).next().css("display", "none");
            }
        });
    }
}
