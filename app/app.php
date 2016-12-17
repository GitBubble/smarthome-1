<?php
error_reporting(E_ALL);
date_default_timezone_set('Europe/Copenhagen');
// Scan all sensors and get a list
// $return = json_decode(shell_exec('python ../services/philips-hue/app.py mode=sensor do=scan'));
// print_r($return);

$run = true;
while($run) {
  $return = json_decode(shell_exec('python ../services/philips-hue/app.py mode=sensor do=get num=15'));
  // print_r($return);
  echo "Activity in this room? ". ($return->state->presence ? 'Yes' : 'No') ."\n";
  sleep(1);
}
?>
