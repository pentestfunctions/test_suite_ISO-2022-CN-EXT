<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];
    $charset = '';

    // Check for common charset parameter names
    $charset_params = [
        'charset', 'encoding', 'target_charset', 'target_encoding',
        'output_charset', 'output_encoding', 'input_charset', 'input_encoding',
        'conversion_charset', 'conversion_encoding'
    ];

    foreach ($charset_params as $param) {
        if (isset($_POST[$param])) {
            $charset = $_POST[$param];
            break;
        }
    }

    // Using iconv to convert input to the specified charset
    if (!empty($charset)) {
        $converted_username = iconv('UTF-8', $charset, $username);
        $converted_password = iconv('UTF-8', $charset, $password);

        if ($converted_username === false || $converted_password === false) {
            echo "Conversion failed";
        } else {
            echo "Username: " . htmlspecialchars($converted_username, ENT_QUOTES, 'UTF-8') . "<br>";
            echo "Password: " . htmlspecialchars($converted_password, ENT_QUOTES, 'UTF-8');
        }
    } else {
        echo "No valid charset parameter found.";
    }
}
?>
