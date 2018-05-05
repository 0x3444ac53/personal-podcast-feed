<?php
$items = array();
$sub = "";
$dir=opendir("./".$sub);

while(($file = readdir($dir)) !== false)
{
        $ext = strtoupper(pathinfo($sub.$file, PATHINFO_EXTENSION));
        if($file !== '.' && $file !== '..' && !is_dir($file) && $ext !== '' && strpos($allowed_ext, $ext)>0)
        {
                $item['name'] = $sub.$file;
                $item['timestamp'] = filectime($sub.$file);
                $item['size'] = filesize($sub.$file);
                $items[] = $item;
        }
}
closedir($dir);
// natcasesort($files); - we will use dates and times to sort the list.
foreach($items as $item) {
        if($item['name'] != "index.php") {
          if (!empty($item['name'])) {
                echo "  <item>\n";
                echo "          <title>". $item['name'] ."</title>\n";
                echo "          <enclosure url='". $feedBaseURL . $item['name']. "' length='" . $item['size'] . "' type='video/mp4' />\n";
                echo "          <guid>". $feedBaseURL . $item['name'] . "</guid>\n";
                echo "          <pubDate>". date(DATE_RFC822, $item['timestamp']) ."</pubDate>\n";
                //echo "                <pubDate>" . $files[$i]['timestamp'] ."</pubDate>\n";
                echo "    </item>\n";
          }
        }
}
?>
