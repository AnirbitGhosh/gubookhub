$(document).ready(function () {

    $('#course-search-input').keyup(function () {
        var query;
        query = $(this).val();
        subject = $(this).attr('name');

        $.get(
            '/gubookhub_app/suggest_courses/',
            { 'suggestion': query, 'subject': subject },
            function (data) {
                $('#course-listing').html(data);
            }
        )
    });

    $('#subject-search-input').keyup(function () {
        var query;
        query = $(this).val();

        $.get(
            '/gubookhub_app/suggest_subjects/',
            { 'suggestion': query,},
            function (data) {
                $('#subject-listing').html(data);
            }
        )
    });

    $('.btn-fav-class').click(function() {
        var book_id;
        book_id = $(this).attr('data-bookid');

        $.get(
            '/gubookhub_app/favourite_book/',
            {'book_id':book_id},
            function(data){
                if (data == '-2'){
                    alert("Item already in your favourites list.");
                } else {
                    $('#' + book_id + '-fav-count').html(data);
                    $('#' + book_id + '-fav-btn').hide();
                }
            }
        )
    });

    $('.btn-subject-info').on('click', function() {
        var subject_slug;
        subject_slug = $(this).attr('data-subject');

        $.getJSON(
            '/gubookhub_app/subject_more_info/',
            {'subject':subject_slug},
            function(data){
                $('#'+subject_slug+"-no-courses").html(data.number_of_courses + " total courses.");
                $('#'+subject_slug+"-no-books").html(data.number_of_books + " total books.");
                $('#'+subject_slug+"-no-awards").html(data.number_of_favs + " total book awards.");
            }
        )
    });

});