<?
header('Content-type: text/xml');
/*
  Runs from a directory containing files to provide an
  RSS 2.0 feed that contains the list and modification times for all the
  files.

*/
$feedName = "My Audio Feed";
$feedDesc = "Feed for the my audio files in some server folder";
$feedURL = "http://www.mysite.com/audio";
$feedBaseURL = "http://www.mysite.com/audio/"; // must end in trailing forward slash (/).

$allowed_ext = ".mp4,.MP4,.mp3,.MP3";

?><<?= '?'; ?>xml version="1.0"<?= '?'; ?>>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title><?=$feedName?></title>
    <link><?=$feedURL?></link>
    <description><?=$feedDesc?></description>
    <atom:link href="http://gogglesoptional.com/bloopers" rel="self" type="application/rss+xml" />
<?
$files = array();
$dir=opendir("./");

while(($file = readdir($dir)) !== false)  
{  
  $path_info = pathinfo($file);
  $ext = strtoupper($path_info['extension']);

  if($file !== '.' && $file !== '..' && !is_dir($file) && strpos($allowed_ext, $ext)>0)  
  {  
    $files[]['name'] = $file;  
    $files[]['timestamp'] = filectime($file);
  }  
}  
closedir($dir);
// natcasesort($files); - we will use dates and times to sort the list.

for($i=0; $i<count($files); $i++) {
  if($files[$i] != "index.php") {
          if (!empty($files[$i]['name'])) {
    echo "  <item>\n";
    echo "    <title>". $files[$i]['name'] ."</title>\n";
    echo "    <link>". $feedBaseURL . $files[$i]['name'] . "</link>\n";
    echo "    <guid>". $feedBaseURL . $files[$i]['name'] . "</guid>\n";
//    echo "    <pubDate>". date("D M j G:i:s T Y", $files[$i]['timestamp']) ."</pubDate>\n";
//    echo "    <pubDate>" . $files[$i]['timestamp'] ."</pubDate>\n";

    echo "    </item>\n";
    }
  }
}
?>
  </channel>
</rss>