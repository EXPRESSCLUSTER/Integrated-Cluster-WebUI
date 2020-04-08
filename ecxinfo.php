<?php

$ini = parse_ini_file('config.ini', TRUE);
$clusternum = count($ini);

for ($i = 1; $i <= $clusternum; $i++) {
	#get clustername and clusterstatus
	$command = $output = NULL;
	$command="python python/cluster_cls.py $i";
	exec($command,$output);

	${'clsname'.$i} = substr($output[0], 0, strcspn($output[0], ' '));
	$output[0] = str_replace(${'clsname'.$i},'',$output[0]);
	${'clsstatus'.$i} = str_replace(':','',$output[0]);

	#get srvname, srvstatus
	$command = $output = NULL;
	$command="python python/cluster_srv.py $i";
	exec($command,$output);
	${'srvcnt'.$i} = count($output);
	$z = 0;
	for ($j = 1; $j <= ${'srvcnt'.$i}; $j++) {
		${'srvname'.$i.'_'.$j} = substr($output[$z], 0, strcspn($output[$z], ' '));
		$output[$z] = str_replace(${'srvname'.$i.'_'.$j},'',$output[$z]);
		${'srvstatus'.$i.'_'.$j} = str_replace(':','',$output[$z]);
		${'srvstatus'.$i.'_'.$j} = ltrim(${'srvstatus'.$i.'_'.$j});
		$z++;
	}

	#get grpname, grpstatus
	$command = $output = NULL;
	$command="python python/cluster_grp.py $i";
	exec($command,$output);
	${'grpcnt'.$i} = count($output) / 2;
	$z = 0;
	for ($j = 1; $j <= ${'grpcnt'.$i}; $j++) {
		$output[$z] = str_replace('current','',$output[$z]);
		$crtgrpsrv = str_replace(':','',$output[$z]);
		$z++;
		${'grpname'.$i.'_'.$j} = substr($output[$z], 0, strcspn($output[$z], ' '));
		$output[$z] = str_replace(${'grpname'.$i.'_'.$j},'',$output[$z]);
		$grpstatus = str_replace(':','',$output[$z]);

		for ($s = 1; $s <= ${'srvcnt'.$i}; $s++) {
			if (strpos($crtgrpsrv, ${'srvname'.$i.'_'.$s}) !== false) {
				${'grpstatus'.$i.'_'.$j.'_'.$s} = $grpstatus;
			} else {
				${'grpstatus'.$i.'_'.$j.'_'.$s} = '-';
			}
		}
		$z++;
	}

	#get rscname, rscstatus
	$command = $output = NULL;
	$command="python python/cluster_rsc.py $i";
	exec($command,$output);
	${'rsccnt'.$i} = count($output) / 2;

	$z = 0;
	for ($j = 1; $j <= ${'rsccnt'.$i}; $j++) {
		$output[$z] = str_replace('current','',$output[$z]);
		$crtrscsrv = str_replace(':','',$output[$z]);
		$z++;
		${'rscname'.$i.'_'.$j} = substr($output[$z], 0, strcspn($output[$z], ' '));
		$output[$z] = str_replace(${'rscname'.$i.'_'.$j},'',$output[$z]);
		$rscstatus = str_replace(':','',$output[$z]);

		for ($s = 1; $s <= ${'srvcnt'.$i}; $s++) {
			if (strpos($crtrscsrv, ${'srvname'.$i.'_'.$s}) !== false) {
				${'rscstatus'.$i.'_'.$j.'_'.$s} = $rscstatus;
			} else {
				${'rscstatus'.$i.'_'.$j.'_'.$s} = '-';
			}
		}
		$z++;
	}

	#get monname, monstatus
	$command = $output = NULL;
	$command="python python/cluster_mon.py $i";
	exec($command,$output);
	${'moncnt'.$i} = count($output) / ((int)${'srvcnt'.$i} + 1);

	$z = 0;
	for ($j = 1; $j <= ${'moncnt'.$i}; $j++) {
		if ($z % ((int)${'srvcnt'.$i} + 1) == 0) {
			${'monname'.$i.'_'.$j} = substr($output[$z], 0, strcspn($output[$z], ' '));
			$z++;
		} 
		for ($s = 1; $s <= ${'srvcnt'.$i}; $s++) {
			if($z % ((int)${'srvcnt'.$i} + 1) != 0) {
				$output[$z] = str_replace(${'srvname'.$i.'_'.$s},'',$output[$z]);
				${'monstatus'.$i.'_'.$j.'_'.$s} = str_replace(':','',$output[$z]);
				${'monstatus'.$i.'_'.$j.'_'.$s} = ltrim(${'monstatus'.$i.'_'.$j.'_'.$s});
				if (strcmp(${'monstatus'.$i.'_'.$j.'_'.$s}, "Offline") == 0) {
					${'monstatus'.$i.'_'.$j.'_'.$s} = "-";
				}
				$z++;
			}
		}
	}
}

?>
 
<!DOCTYPE html>
<html>
<head>
<title> EXPRESSCLUSTER Information </title>
<meta charset="utf-8">
</head>
<body>

<h1> EXPRESSCLUSTER Information </h1>

<font size=5> 
<table border='0'>
<meta http-equiv="refresh" content="60" >
<?php 
for ($i = 1; $i <= $clusternum; $i++) {
?>
<td valign="top">
	<table border='1' style="float:left;margin:25px;">
		<h3> <?php echo ${'clsname'.$i} ?> is <?php echo ${'clsstatus'.$i} ?> </h3>
		<tr><th> </th> 
		<?php
			for ($j = 1; $j <= ${'srvcnt'.$i}; $j++) {
		?>
				<th><?php echo ${'srvname'.$i.'_'.$j} ?></th>
		<?php
			}
		?>
		</tr>

		<tr><th> status </th> 
		<?php
			for ($j = 1; $j <= ${'srvcnt'.$i}; $j++) {
		?>
				<th><?php echo ${'srvstatus'.$i.'_'.$j} ?></th>
		<?php
			}
		?>
		</tr>

		
		<?php
			for ($j = 1; $j <= ${'grpcnt'.$i}; $j++) {
		?>
				<tr><th> <?php echo ${'grpname'.$i.'_'.$j} ?> </th>
			<?php
				for ($s = 1; $s <= ${'srvcnt'.$i}; $s++) {
			?>
					<th> <?php echo ${'grpstatus'.$i.'_'.$j.'_'.$s} ?> </th>
			<?php
				}
			?>
			</tr>
		<?php
			}
		?>

		<?php
			for ($j = 1; $j <= ${'rsccnt'.$i}; $j++) {
		?>
				<tr><td align="right"> <?php echo ${'rscname'.$i.'_'.$j} ?> </td>
			<?php
				for ($s = 1; $s <= ${'srvcnt'.$i}; $s++) {
			?>
					<th> <?php echo ${'rscstatus'.$i.'_'.$j.'_'.$s} ?> </th>
			<?php
				}
			?>
			</tr>
		<?php
			}
		?>

		<?php
			for ($j = 1; $j <= ${'moncnt'.$i}; $j++) {
		?>
				<tr><th> <?php echo ${'monname'.$i.'_'.$j} ?> </th>
			<?php
				for ($s = 1; $s <= ${'srvcnt'.$i}; $s++) {
			?>
					<th> <?php echo ${'monstatus'.$i.'_'.$j.'_'.$s} ?> </th>
			<?php
				}
			?>
			</tr>
		<?php
			}
		?>

	</table>
</td>

<?php
}
?>

</font>

<FORM>
<INPUT TYPE="image" src="image/kurara.png" VALUE="reload"onClick="window.location.reload(); "style="position: absolute; right: 0px; top: 0px"/>
</FORM>
</body>
</html>
