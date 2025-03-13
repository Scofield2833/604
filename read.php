<?php
$servername = "sql100.infinityfree.com";
$username = "if0_37969262";
$password = "nySeh0vNYuw";
$dbname = "if0_37969262_441week4";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: ". $conn->connect_error);
}

$sql = "SELECT * FROM timetables";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    echo "<h2>Time Table</h2>";
    echo "<table border='1'>
            <tr>
                <th>Subject</th>
                <th>Day</th>
                <th>Time</th>
                <th>Teacher</th>
            </tr>";
    while($row = $result->fetch_assoc()) {
        echo "<tr>
                <td>". $row['subject']. "</td>
                <td>". $row['day']. "</td>
                <td>". $row['time']. "</td>
                <td>". $row['teacher']. "</td>
              </tr>";
    }
    echo "</table>";
} else {
    echo "0 results";
}

$conn->close();
?>