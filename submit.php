<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $to = "harikamkhs@gmail.com";  // Your email address
    $subject = "New Contact Form Submission";

    $email = filter_var($_POST["email"], FILTER_SANITIZE_EMAIL);
    $message = htmlspecialchars($_POST["message"]);

    $body = "From: $email\n\nMessage:\n$message";
    $headers = "From: $email";

    // Send the email
    if (mail($to, $subject, $body, $headers)) {
        // Redirect to thank you or home page
        header("Location: index.html");
        exit();
    } else {
        echo "Something went wrong. Please try again later.";
    }
} else {
    // Prevent direct access
    header("Location: contact.html");
    exit();
}
?>
