$(document).ready(function () {

    $('.content-section').hide();
    $('.methods').show();
    var heading = $('.heading-link[data-section="methods"]');
    heading.css('background', '#849627');
    heading.css('color', 'white');

    function openNav() {
        document.getElementById("mySidenav").style.width = "27%";
        document.getElementById("main").style.marginLeft = "27%";
    }

    function closeNav() {
        document.getElementById("mySidenav").style.width = "0%";
        document.getElementById("main").style.marginLeft = "0%";
    }


    $('.sidenav a').click(function () {
            $('.sidenav a').css('background', '#11111100');
            $('.sidenav a').css('color', '#818181');
            if ($(this).hasClass('heading-link')) {
                $('.content-section').hide();
                if ($(this).attr('data-section') === 'policies') {
                    var subheading = $('a[data-section="ht_2050"]')
                    subheading.css('background', '#849627');
                    subheading.css('color', 'white');
                    $('.content-section.policies').show();
                    $('.content-section.policies .subcontent').hide();
                    $('.content-section .subcontent.ht_2050').show();
                }
                $('.content-section.' + $(this).attr('data-section')).show();
            } else if ($(this).parent().hasClass('sub-heading-link')) {
                var policies_heading = $('a[data-section="policies"]')
                policies_heading.css('background', '#849627');
                policies_heading.css('color', 'white');
                $('.content-section').hide();
                $('.content-section.policies div.subcontent').hide();
                $('.subcontent.' + $(this).attr('data-section')).show();
                $('.content-section.policies').show();
            }

            $(this).not(document.getElementsByClassName("closebtn")).css('background', '#849627');
            $(this).not(document.getElementsByClassName("closebtn")).css('color', 'white');
        }
    );

    $('.content_btn').on('click', function () {
        if (document.getElementById("mySidenav").style.width !== '0%') {
            closeNav();
        } else {
            openNav();
        }
    });
    openNav();

});