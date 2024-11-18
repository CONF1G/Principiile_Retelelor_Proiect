<?php
// Codul pentru clientul UDP
$udp_ip = "127.0.0.1";
$udp_port = 12346;

$socket = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);  // Crearea socketului UDP
if (!$socket) {
    die("Eroare la crearea socketului UDP\n");
}
$s = 0;
while (true) {
    if ($s == 0) {
        echo "Apasa Enter\n";
        $s++;
    }
    else
    {
        echo "Introdu un număr: ";
    }

    $input = trim(fgets(STDIN));  // Citirea inputului utilizatorului
    socket_sendto($socket, $input, strlen($input), 0, $udp_ip, $udp_port);  // Trimiterea mesajului la server

    $response = "";
    socket_recvfrom($socket, $response, 1024, 0, $udp_ip, $udp_port);  // Primirea răspunsului de la server
    echo $response . "\n";  // Afișarea răspunsului de la server

    if (strpos($response, "Felicitari") !== false) {  // Condiția de oprire
        break;
    }
}

socket_close($socket);  // Închiderea socketului


?>
