<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name   = strip_tags(trim($_POST["name"]));
    $age    = strip_tags(trim($_POST["age"]));
    $mobile = strip_tags(trim($_POST["mobile"]));
    $email  = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
    $date   = $_POST["date"];
    $time   = $_POST["time"];
    $mode   = $_POST["mode"];

    $to = "ask@tattvainvestmentadvisory.com, harika@tattvainvestmentadvisory.com";
    $subject = "New Appointment Booking - Tattva Capital";

    $message = "
    You have received a new appointment request:\n\n
    Name: $name\n
    Age: $age\n
    Mobile: $mobile\n
    Email: $email\n
    Preferred Date: $date\n
    Preferred Time: $time\n
    Mode of Meeting: $mode\n
    ";

    $headers = "From: $email";

    if (mail($to, $subject, $message, $headers)) {
        header("Location:thank.html");  // Optional redirect
        exit;
    } else {
        echo "Something went wrong. Please try again.";
    }
} else {
    echo "Unauthorized access.";
}
?>
