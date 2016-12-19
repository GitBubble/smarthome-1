<?php
require('config.php');

$method = $_SERVER['REQUEST_METHOD'];
$request = explode('/', trim($_SERVER['REQUEST_URI'],'/'));
$input = json_decode(file_get_contents('php://input'),true);

$controller_path = 'controller/'. implode($request,'/') .'.php';

if(file_exists($controller_path)) {
  require($controller_path);
  $method_func = strtolower($method);
  $object = new Obj();

  if(method_exists($object,$method_func)) {
    echo json_encode($object->$method_func());
  } else {
    echo json_encode([
      'status' => 404,
      'error' => _('method are not found for this command.')
    ]);
  }
} else {
  echo json_encode([
    'status' => 404,
    'error' => _('command are not found.')
  ]);
}
?>
