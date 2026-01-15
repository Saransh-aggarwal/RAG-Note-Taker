/* RAG Chatbot - Main JavaScript */

$(document).ready(function () {
    // Close alert messages
    $('.alert-close').on('click', function () {
        $(this).closest('.alert').fadeOut(200, function () {
            $(this).remove();
        });
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function () {
        $('.alert').fadeOut(300, function () {
            $(this).remove();
        });
    }, 5000);
});
