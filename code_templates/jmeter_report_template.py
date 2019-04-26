# -*- encoding:utf-8 -*-

jmeter_report_template_dict = {
    "jmeter_report_index_template": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <title>Apache JMeter Dashboard</title>
     <!-- Bootstrap Core CSS -->
    <link href="sbadmin2-1.0.7/bower_components/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- MetisMenu CSS -->
    <link href="sbadmin2-1.0.7/bower_components/metisMenu/dist/metisMenu.min.css" rel="stylesheet">
    <!-- Custom CSS -->
    <link href="sbadmin2-1.0.7/dist/css/sb-admin-2.css" rel="stylesheet">
    <!-- Dashboard css -->
    <link href="content/css/dashboard.css" rel="stylesheet">
    <!-- Table sorter -->
    <link href="content/css/theme.blue.css" rel="stylesheet">
    <!-- icon -->
    <link rel="icon" type="image/png" href="content/pages/icon-apache.png" />
    <!-- Custom Fonts -->
    <link href="sbadmin2-1.0.7/bower_components/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
</head>

<body>
    <div id="wrapper">
        <nav class="navbar navbar-default navbar-static-top" role="navigation" style="margin-bottom: 0">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="index-{{ mission_id }}.html">Apache JMeter Dashboard</a>
            </div>
            <div class="navbar-default sidebar" role="navigation">
                <div class="sidebar-nav navbar-collapse">
                    <ul class="nav" id="side-menu">
                        <li>
                            <a href="index-{{ mission_id }}.html"><i class="fa fa-dashboard fa-fw"></i> Dashboard</a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-bar-chart-o fa-fw"></i> Charts<span class="fa arrow"></span></a>
                            <ul class="nav nav-second-level">
                                <li>
                                    <a href="content/pages/OverTime-{{ mission_id }}.html">Over Time</a>
                                </li>
                                <li>
                                    <a href="content/pages/Throughput-{{ mission_id }}.html">Throughput</a>
                                </li>
                                <li>
                                    <a href="content/pages/ResponseTimes-{{ mission_id }}.html">Response Times</a>
                                </li>
                            </ul>
                            <!-- /.nav-second-level -->
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
        <div id="page-wrapper">
            <div class="row">
                <div class="col-lg-12">
                     <div class="panel panel-default" >
                        <div class="panel-heading" style="text-align:center;">
                           <p class="dashboard-title">Test and Report informations</p>
                        </div>
                        <div class="panel-body">
                        <table id="generalInfos" class="table table-bordered table-condensed " >
                            <tr>
                                <td>File:</td>
                                <td>"LoadTest.1.jtl"</td>
                            </tr>
                            <tr>
                                <td>Start Time:</td>
                                <td>"18-8-2 下午10:05"</td>
                            </tr>
                            <tr>
                                <td>End Time:</td>
                                <td>"18-8-2 下午10:05"</td>
                            </tr>
                                <tr>
                                    <td>Filter for display:</td>
                                    <td>""</td>
                                </tr>
                        </table>
                     </div>
                </div>
            </div>
            <div class="row">
                <div class="col-lg-6">
                    <div class="panel panel-default" style="text-align:center;">
                        <div class="panel-heading">
                           <p class="dashboard-title"><a href="https://en.wikipedia.org/wiki/Apdex" target="_blank">APDEX (Application Performance Index)</a></p>
                        </div>
                        <div class="panel-body">
                            <section id="apdex" class="col-md-12 table-responsive">
                                <table id="apdexTable" class="table table-bordered table-condensed tablesorter ">
                                </table>
                            </section>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6" >
                    <div class="panel panel-default" style="text-align:center;">
                        <div class="panel-heading">
                           <p class="dashboard-title">Requests Summary</p>
                        </div>
                           <div class="panel-body">
                            <div class="flot-chart" style="height:200px;">
                                <div class="flot-chart-content" id="flot-requests-summary" style="height:200px;"/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-lg-12">
                <div class="panel panel-default" style="text-align:center;">
                       <div class="panel-heading" >
                           <p class="dashboard-title">Statistics</p>
                       </div>
                <div class="panel-body ">
                    <section class="col-md-12 table-responsive">
                        <table id="statisticsTable" class="table table-bordered table-condensed tablesorter " >
                        </table>
                    </section>
                </div>
            </div>
            <div class="col-lg-12">
                <div class="panel panel-default" style="text-align:center;">
                    <div class="panel-heading">
                        <p class="dashboard-title">Errors</p>
                    </div>
                    <div class="panel-body">
                        <section class="col-md-12 table-responsive">
                            <table id="errorsTable" class="table table-bordered table-condensed tablesorter ">
                            </table>
                        </section>
                    </div>
                </div>
            </div>
            <div class="col-lg-12">
                <div class="panel panel-default" style="text-align:center;">
                    <div class="panel-heading">
                        <p class="dashboard-title">Top 5 Errors by sampler</p>
                    </div>
                    <div class="panel-body">
                        <section class="col-md-12 table-responsive">
                            <table id="top5ErrorsBySamplerTable" class="table table-bordered table-condensed tablesorter ">
                            </table>
                        </section>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- jQuery -->
    <script src="sbadmin2-1.0.7/bower_components/jquery/dist/jquery.min.js"></script>
    <!-- Bootstrap Core JavaScript -->
    <script src="sbadmin2-1.0.7/bower_components/bootstrap/dist/js/bootstrap.min.js"></script>
    <script src="sbadmin2-1.0.7/bower_components/flot/excanvas.min.js"></script>
    <script src="sbadmin2-1.0.7/bower_components/flot/jquery.flot.js"></script>
    <script src="sbadmin2-1.0.7/bower_components/flot/jquery.flot.pie.js"></script>
    <script src="sbadmin2-1.0.7/bower_components/flot/jquery.flot.resize.js"></script>
    <script src="sbadmin2-1.0.7/bower_components/flot/jquery.flot.time.js"></script>
    <script src="sbadmin2-1.0.7/bower_components/flot.tooltip/js/jquery.flot.tooltip.min.js"></script>
    <script src="sbadmin2-1.0.7/bower_components/flot-axislabels/jquery.flot.axislabels.js"></script>
    <!-- Metis Menu Plugin JavaScript -->
    <script src="sbadmin2-1.0.7/bower_components/metisMenu/dist/metisMenu.min.js"></script>
    <script src="content/js/dashboard-commons.js"></script>
    <script src="content/js/dashboard-{{ mission_id }}.js"></script>
    <!-- Custom Theme JavaScript -->
    <script src="sbadmin2-1.0.7/dist/js/sb-admin-2.js"></script>
    <script type="text/javascript" src="content/js/jquery.tablesorter.min.js"></script>
</body>
</html>
""",
    "OverTime": """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Apache JMeter Dashboard</title>

    <!-- Bootstrap Core CSS -->
    <link href="../../sbadmin2-1.0.7/bower_components/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- icone onglet -->
    <link rel="icon" type="image/png" href="icon-apache.png" />

    <!-- MetisMenu CSS -->
    <link href="../../sbadmin2-1.0.7/bower_components/metisMenu/dist/metisMenu.min.css" rel="stylesheet">

    <!-- Legends CSS -->
    <link href="../css/legends.css" rel="stylesheet">


    <!-- Custom CSS -->
    <link href="../../sbadmin2-1.0.7/dist/css/sb-admin-2.css" rel="stylesheet">

    <!-- Custom Fonts -->
    <link href="../../sbadmin2-1.0.7/bower_components/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">

   <!-- JQuery UI style -->
    <link href="../css/jquery-ui.css" rel="stylesheet">
    <link href="../css/jquery-ui.structure.css" rel="stylesheet">
    <link href="../css/jquery-ui.theme.css" rel="stylesheet">
</head>

<body>

    <div id="wrapper">

        <!-- Navigation -->
        <nav class="navbar navbar-default navbar-static-top" role="navigation" style="margin-bottom: 0">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="../../index-{{ mission_id }}.html">Apache JMeter Dashboard</a>
            </div>
            <!-- /.navbar-header -->


            <div class="navbar-default sidebar" role="navigation">
                <div class="sidebar-nav navbar-collapse">
                    <ul class="nav" id="side-menu">

                        <li>
                            <a href="../../index-{{ mission_id }}.html"><i class="fa fa-dashboard fa-fw"></i> Dashboard</a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-bar-chart-o fa-fw"></i> Charts<span class="fa arrow"></span></a>
                            <ul class="nav nav-second-level">
                                <li>
                                    <a href="OverTime-{{ mission_id }}.html">Over Time<span class="fa arrow"></span></a>
                                    <ul class="nav nav-third-level in" id="submenu">
                                        <li>
                                            <a href="OverTime-{{ mission_id }}.html#responseTimesOverTime" onclick="$('#bodyResponseTimeOverTime').collapse('show');">
                                                Response Times Over Time
                                            </a>
                                        </li>
                                        <li>
                                            <a href="OverTime-{{ mission_id }}.html#responseTimePercentilesOverTime" onclick="$('#bodyResponseTimePercentilesOverTime').collapse('show');">
                                                Response Time Percentiles Over Time (successful responses)
                                            </a>
                                        </li>
                                        <li>
                                            <a href="OverTime-{{ mission_id }}.html#activeThreadsOverTime" onclick="$('#bodyActiveThreadsOverTime').collapse('show');">
                                                Active Threads Over Time
                                            </a>
                                        </li>
                                        <li>
                                            <a href="OverTime-{{ mission_id }}.html#bytesThroughputOverTime" onclick="$('#bodyBytesThroughputOverTime').collapse('show');">
                                                Bytes Throughput Over Time
                                            </a>
                                        </li>
                                        <li>
                                            <a href="OverTime-{{ mission_id }}.html#latenciesOverTime" onclick="$('#bodyLatenciesOverTime').collapse('show');">
                                                Latencies Over Time
                                            </a>
                                        </li>
                                        <li>
                                            <a href="OverTime-{{ mission_id }}.html#connectTimeOverTime" onclick="$('#bodyConnectTimeOverTime').collapse('show');">
                                                Connect Time Over Time
                                            </a>
                                        </li>
                                    </ul>
                                </li>
                                <li>
                                    <a href="Throughput-{{ mission_id }}.html">Throughput</a>
                                </li>
                                <li>
                                    <a href="ResponseTimes-{{ mission_id }}.html">Response Times</a>
                                </li>
                            </ul>
                            <!-- /.nav-second-level -->
                        </li>

                    </ul>
                </div>
                <!-- /.sidebar-collapse -->
            </div>
            <!-- /.navbar-static-side -->
        </nav>
        <!--modal-->
        <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
          <div class="modal-dialog" style="width:90%;height: 5%;">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title" id="myModalLabel">Zoom</h4>
              </div>
              <div class="modal-body">
                <div class="flot-chart">
                    <div class="flot-chart-content" id="flot-modal-content"></div>
                </div>
              </div>
              <div class="modal-footer" id="modalFooter">
                <p id="legendModal" hidden></p>
                <ul id="choicesModal" class="legend"></ul>
              </div>
            </div>
          </div>
        </div>

        <div id="page-wrapper">
            <div class="row">
                <div class="col-lg-12">
                     <div class="panel panel-default" >
                        <div class="panel-heading" style="text-align:center;">
                           <p class="dashboard-title">Test and Report informations</p>
                        </div>
                        <div class="panel-body">
                        <table id="generalInfos" class="table table-bordered table-condensed " >
                            <tr>
                                <td>File:</td>
                                <td>"LoadTest.1.jtl"</td>
                            </tr>
                            <tr>
                                <td>Start Time:</td>
                                <td>"18-8-2 下午10:05"</td>
                            </tr>
                            <tr>
                                <td>End Time:</td>
                                <td>"18-8-2 下午10:05"</td>
                            </tr>
                                <tr>
                                    <td>Filter for display:</td>
                                    <td>""</td>
                                </tr>
                        </table>
                     </div>
                </div>
            </div>
            <!-- /.row -->
            <div class="row" id="graphContainer">

            <!-- /.col-lg-6 -->
            <div class="col-lg-12 portlet" id="responseTimesOverTime">
                    <div class="panel panel-default">
                        <div class="panel-heading portlet-header">
                             <i  class="fa fa-bar-chart-o fa-fw" ></i> 
                            <span type="button" class="span-title dropdown-toggle click-title" data-toggle="collapse" href="#bodyResponseTimeOverTime" aria-expanded="true" aria-controls="bodyResponseTimeOverTime">Response Times Over Time</span>
                             <div class="pull-right">
                                <div class="btn-group">
                                    <a class="btn btn-link btn-xs">
                                        <i class="glyphicon glyphicon-resize-vertical"></i>
                                    </a>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="dropdown">
                                        <i class="fa fa-wrench"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-user">
                                        <li><a href="#bodyResponseTimeOverTime" onClick="checkAll('choicesResponseTimesOverTime');">Display all samples</a>
                                        </li>
                                        <li><a href="#bodyResponseTimeOverTime" onClick="uncheckAll('choicesResponseTimesOverTime');">Hide all samples</a>
                                        </li>
                                        <li><a href="#bodyResponseTimeOverTime" onclick="exportToPNG('flotResponseTimesOverTime', this);">Save as PNG</a></li>
                                    </ul>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="collapse" href="#bodyResponseTimeOverTime" aria-expanded="true" aria-controls="bodyResponseTimeOverTime">
                                        <i class="fa fa-chevron-up"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="collapse in portlet-content" id="bodyResponseTimeOverTime">
                            <div class="panel-body" id="collapseResponseTimesOverTime">
                                <div class="flot-chart">
                                    <div class="flot-chart-content" id="flotResponseTimesOverTime" style="float: left; width:80%;"></div>
                                    <div style="float:left;margin-left:5px">
                                        <p>Zoom :</p>
                                        <div id="overviewResponseTimesOverTime" style="width:190px;height:100px;"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="panel-footer" id="footerResponseTimesOverTime">
                                <p id="legendResponseTimesOverTime" hidden></p>
                                <ul id="choicesResponseTimesOverTime" class="legend"></ul>
                            </div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
                <!-- /.col-lg-12 -->
                
                <!-- /.col-lg-12 -->
                <div class="col-lg-12 portlet" id="responseTimePercentilesOverTime">
                    <div class="panel panel-default">
                        <div class="panel-heading portlet-header">
                            <i class="fa fa-bar-chart-o fa-fw"></i>
                            <span type="button" class="dropdown-toggle click-title span-title" data-toggle="collapse" href="#bodyResponseTimePercentilesOverTime" aria-expanded="true" aria-controls="bodyResponseTimePercentilesOverTime">Response Time Percentiles Over Time (successful responses)</span>
                            <div class="pull-right">
                                <div class="btn-group">
                                    <a class="btn btn-link btn-xs">
                                        <i class="glyphicon glyphicon-resize-vertical"></i>
                                    </a>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="dropdown">
                                        <i class="fa fa-wrench"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-user">
                                        <li><a href="#responseTimePercentilesOverTime" onClick="checkAll('choicesResponseTimePercentilesOverTime');">Display all samples</a>
                                        </li>
                                        <li><a href="#responseTimePercentilesOverTime" onClick="uncheckAll('choicesResponseTimePercentilesOverTime');">Hide all samples</a>
                                        </li>
                                        <li><a href="#responseTimePercentilesOverTime" onclick="exportToPNG('flotResponseTimePercentilesOverTime', this);">Save as PNG</a></li>
                                    </ul>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="collapse" href="#bodyResponseTimePercentilesOverTime" aria-expanded="true" aria-controls="bodyResponseTimePercentilesOverTime">
                                        <i class="fa fa-chevron-down"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="collapse out portlet-content" id="bodyResponseTimePercentilesOverTime">
                            <div class="panel-body" id="collapseConnectTime">
                                <div class="flot-chart">
                                    <div class="flot-chart-content" id="flotResponseTimePercentilesOverTime" style="float: left; width:80%;"></div>
                                    <div style="float:left;margin-left:5px">
                                        <p>Zoom :</p>
                                        <div id="overviewResponseTimePercentilesOverTime" style="width:190px;height:100px;"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="panel-footer" id="footerResponseTimePercentilesOverTime">
                                    <p id="legendResponseTimePercentilesOverTime" hidden></p>
                                    <ul id="choicesResponseTimePercentilesOverTime" class="legend"></ul>
                            </div>
                        </div>
                        <!-- /.panel-body -->

                    </div>
                    <!-- /.panel -->
                </div>
                <!-- /.col-lg-12 -->
                
                <div class="col-lg-12 portlet" id="activeThreadsOverTime">
                    <div class="panel panel-default" >
                        <div class="panel-heading portlet-header">
                           <i class="fa fa-bar-chart-o fa-fw"> </i>  <span type="button" class="span-title dropdown-toggle click-title" data-toggle="collapse" href="#bodyActiveThreadsOverTime" aria-expanded="true" aria-controls="bodyActiveThreadsOverTime">Active Threads Over Time</span>
                           <div class="pull-right">
                                <div class="btn-group">
                                    <a class="drag btn btn-link btn-xs">
                                        <i class="glyphicon glyphicon-resize-vertical"></i>
                                    </a>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="dropdown">
                                        <i class="fa fa-wrench"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-user">
                                        <li><a href="#activeThreadsOverTime" onClick="checkAll('choicesActiveThreadsOverTime');">Display all samples</a>
                                        </li>
                                        <li><a href="#activeThreadsOverTime" onClick="uncheckAll('choicesActiveThreadsOverTime');">Hide all samples</a>
                                        </li>
                                        <li><a href="#activeThreadsOverTime" onclick="exportToPNG('flotActiveThreadsOverTime', this);">Save as PNG</a></li>
                                    </ul>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="collapse" href="#bodyActiveThreadsOverTime" aria-expanded="true" aria-controls="bodyActiveThreadsOverTime">
                                        <i class="fa fa-chevron-down"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="collapse out portlet-content" id="bodyActiveThreadsOverTime">
                            <div class="panel-body" id="collapseActiveThreadsOverTime">
                                <div class="flot-chart">
                                    <div class="flot-chart-content" id="flotActiveThreadsOverTime" style="float: left; width:80%;"></div>
                                    <div style="float:left;margin-left:5px">
                                        <p>Zoom :</p>
                                        <div id="overviewActiveThreadsOverTime" style="width:190px;height:100px;"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="panel-footer" id="footerActiveThreadsOverTime">
                                    <p id="legendActiveThreadsOverTime" hidden></p>
                                    <ul id="choicesActiveThreadsOverTime" class="legend">

                                    </ul>
                                </div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
                

                <div class="col-lg-12 portlet" id="bytesThroughputOverTime">
                    <div class="panel panel-default">
                        <div class="panel-heading portlet-header">
                             <i class="fa fa-bar-chart-o fa-fw" ></i> <span type="button" class="dropdown-toggle click-title span-title" data-toggle="collapse" href="#bodyBytesThroughputOverTime" aria-expanded="true" aria-controls="bodyBytesThroughputOverTime">Bytes Throughput Over Time</span>
                           <div class="pull-right">
                                <div class="btn-group">
                                    <a class="btn btn-link btn-xs">
                                        <i class="glyphicon glyphicon-resize-vertical"></i>
                                    </a>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="dropdown">
                                        <i class="fa fa-wrench"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-user">
                                        <li><a href="#bytesThroughputOverTime" onClick="checkAll('choicesBytesThroughputOverTime');">Display all samples</a>
                                        </li>
                                        <li><a href="#bytesThroughputOverTime" onClick="uncheckAll('choicesBytesThroughputOverTime');">Hide all samples</a>
                                        </li>
                                        <li><a href="#bytesThroughputOverTime" onclick="exportToPNG('flotBytesThroughputOverTime', this);">Save as PNG</a></li>
                                    </ul>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="collapse" href="#bodyBytesThroughputOverTime" aria-expanded="true" aria-controls="bodyBytesThroughputOverTime">
                                        <i class="fa fa-chevron-down"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="collapse out portlet-content" id="bodyBytesThroughputOverTime">
                            <div class="panel-body " id="collapseBytes">
                                <div class="flot-chart">
                                    <div class="flot-chart-content" id="flotBytesThroughputOverTime" style="float: left; width:80%;"></div>
                                    <div style="float:left;margin-left:5px">
                                        <p>Zoom :</p>
                                        <div id="overviewBytesThroughputOverTime" style="width:190px;height:100px;"></div>
                                    </div>
                                </div>
                            </div>
                            <!-- /.panel-body -->
                            <div class="panel-footer" id="footerBytesThroughputOverTime">
                                <p id="legendBytesThroughputOverTime" hidden></p>
                                <ul id="choicesBytesThroughputOverTime" class="legend"></ul>
                            </div>
                        </div>
                    </div>
                    <!-- /.panel -->
                </div>

                <!-- /.col-lg-6 -->
                <div class="col-lg-12 portlet" id="latenciesOverTime">
                    <div class="panel panel-default">
                        <div class="panel-heading portlet-header">
                            <i class="fa fa-bar-chart-o fa-fw"></i>
                            <span type="button" class="dropdown-toggle click-title span-title" data-toggle="collapse" href="#bodyLatenciesOverTime" aria-expanded="true" aria-controls="bodyLatenciesOverTime">Latencies Over Time</span>
                            <div class="pull-right">
                                <div class="btn-group">
                                    <a class="btn btn-link btn-xs">
                                        <i class="glyphicon glyphicon-resize-vertical"></i>
                                    </a>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="dropdown">
                                        <i class="fa fa-wrench"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-user">
                                        <li><a href="#latenciesOverTime" onClick="checkAll('choicesLatenciesOverTime');">Display all samples</a>
                                        </li>
                                        <li><a href="#latenciesOverTime" onClick="uncheckAll('choicesLatenciesOverTime');">Hide all samples</a>
                                        </li>
                                        <li><a href="#latenciesOverTime" onclick="exportToPNG('flotLatenciesOverTime', this);">Save as PNG</a></li>
                                    </ul>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="collapse" href="#bodyLatenciesOverTime" aria-expanded="true" aria-controls="bodyLatenciesOverTime">
                                        <i class="fa fa-chevron-down"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="collapse out portlet-content" id="bodyLatenciesOverTime">
                            <div class="panel-body" id="collapseLatencies">
                                <div class="flot-chart">
                                    <div class="flot-chart-content" id="flotLatenciesOverTime" style="float: left; width:80%;"></div>
                                    <div style="float:left;margin-left:5px">
                                        <p>Zoom :</p>
                                        <div id="overviewLatenciesOverTime" style="width:190px;height:100px;"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="panel-footer" id="footerLatenciesOverTime">
                                    <p id="legendLatenciesOverTime" hidden></p>
                                    <ul id="choicesLatenciesOverTime" class="legend"></ul>
                            </div>
                        </div>
                        <!-- /.panel-body -->

                    </div>
                    <!-- /.panel -->
                </div>

                <!-- /.col-lg-6 -->
                <div class="col-lg-12 portlet" id="connectTimeOverTime">
                    <div class="panel panel-default">
                        <div class="panel-heading portlet-header">
                            <i class="fa fa-bar-chart-o fa-fw"></i>
                            <span type="button" class="dropdown-toggle click-title span-title" data-toggle="collapse" href="#bodyConnectTimeOverTime" aria-expanded="true" aria-controls="bodyConnectTimeOverTime">Connect Time Over Time</span>
                            <div class="pull-right">
                                <div class="btn-group">
                                    <a class="btn btn-link btn-xs">
                                        <i class="glyphicon glyphicon-resize-vertical"></i>
                                    </a>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="dropdown">
                                        <i class="fa fa-wrench"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-user">
                                        <li><a href="#connectTimeOverTime" onClick="checkAll('choicesConnectTimeOverTime');">Display all samples</a>
                                        </li>
                                        <li><a href="#connectTimeOverTime" onClick="uncheckAll('choicesConnectTimeOverTime');">Hide all samples</a>
                                        </li>
                                        <li><a href="#connectTimeOverTime" onclick="exportToPNG('flotConnectTimeOverTime', this);">Save as PNG</a></li>
                                    </ul>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="collapse" href="#bodyConnectTimeOverTime" aria-expanded="true" aria-controls="bodyConnectTimeOverTime">
                                        <i class="fa fa-chevron-down"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="collapse out portlet-content" id="bodyConnectTimeOverTime">
                            <div class="panel-body" id="collapseConnectTime">
                                <div class="flot-chart">
                                    <div class="flot-chart-content" id="flotConnectTimeOverTime" style="float: left; width:80%;"></div>
                                    <div style="float:left;margin-left:5px">
                                        <p>Zoom :</p>
                                        <div id="overviewConnectTimeOverTime" style="width:190px;height:100px;"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="panel-footer" id="footerConnectTimeOverTime">
                                    <p id="legendConnectTimeOverTime" hidden></p>
                                    <ul id="choicesConnectTimeOverTime" class="legend"></ul>
                            </div>
                        </div>
                        <!-- /.panel-body -->

                    </div>
                    <!-- /.panel -->
                </div>
                <!-- /.col-lg-6 -->
            </div>
            <!-- /.row -->
        </div>
        <!-- /#page-wrapper -->
    </div>
    <!-- /#wrapper -->
    <!-- jQuery -->
    <script src="../../sbadmin2-1.0.7/bower_components/jquery/dist/jquery.min.js"></script>
    <!-- Bootstrap Core JavaScript -->
    <script src="../../sbadmin2-1.0.7/bower_components/bootstrap/dist/js/bootstrap.min.js"></script>
    <!-- Metis Menu Plugin JavaScript -->
    <script src="../../sbadmin2-1.0.7/bower_components/metisMenu/dist/metisMenu.min.js"></script>
    <!-- Flot Charts JavaScript -->
    <script src="../../sbadmin2-1.0.7/bower_components/flot/excanvas.min.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.pie.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.resize.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.canvas.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.time.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.selection.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot.tooltip/js/jquery.flot.tooltip.min.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot-axislabels/jquery.flot.axislabels.js"></script>
    <script src="../js/jquery.flot.stack.js"></script>
    <script src="../js/hashtable.js"></script>
    <script src="../js/jquery.numberformatter-1.2.3.min.js"></script>
    <script src="../js/curvedLines.js"></script>
    <script src="../js/dashboard-commons.js"></script>
    <script src="../js/graph-{{ mission_id }}.js"></script>
    <script src="../js/jquery-ui.js"></script>
    <script src="../js/jquery.cookie.js"></script>
    <!-- Custom Theme JavaScript -->
    <script src="../../sbadmin2-1.0.7/dist/js/sb-admin-2.js"></script>
</body>
</html>
""",
    "ResponseTimes": """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Apache JMeter Dashboard</title>

    <!-- Bootstrap Core CSS -->
    <link href="../../sbadmin2-1.0.7/bower_components/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- icone onglet -->
    <link rel="icon" type="image/png" href="icon-apache.png" />

    <!-- MetisMenu CSS -->
    <link href="../../sbadmin2-1.0.7/bower_components/metisMenu/dist/metisMenu.min.css" rel="stylesheet">

    <!-- Legends CSS -->
    <link href="../css/legends.css" rel="stylesheet">


    <!-- Custom CSS -->
    <link href="../../sbadmin2-1.0.7/dist/css/sb-admin-2.css" rel="stylesheet">

    <!-- Custom Fonts -->
    <link href="../../sbadmin2-1.0.7/bower_components/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">

   <!-- JQuery UI style -->
    <link href="../css/jquery-ui.css" rel="stylesheet">
    <link href="../css/jquery-ui.structure.css" rel="stylesheet">
    <link href="../css/jquery-ui.theme.css" rel="stylesheet">
</head>

<body>

    <div id="wrapper">

        <!-- Navigation -->
        <nav class="navbar navbar-default navbar-static-top" role="navigation" style="margin-bottom: 0">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="../../index-{{ mission_id }}.html">Apache JMeter Dashboard</a>
            </div>
            <!-- /.navbar-header -->
            <div class="navbar-default sidebar" role="navigation">
                <div class="sidebar-nav navbar-collapse">
                    <ul class="nav" id="side-menu">

                        <li>
                            <a href="../../index-{{ mission_id }}.html"><i class="fa fa-dashboard fa-fw"></i> Dashboard</a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-bar-chart-o fa-fw"></i> Charts<span class="fa arrow"></span></a>
                            <ul class="nav nav-second-level">
                                <li>
                                    <a href="OverTime-{{ mission_id }}.html">Over Time</a>

                                </li>
                                <li>
                                    <a href="Throughput-{{ mission_id }}.html">Throughput</a>
                                </li>
                                <li>
                                    <a href="ResponseTimes-{{ mission_id }}.html">Response Times<span class="fa arrow"></span></a>

                                    <ul class="nav nav-third-level in" id="submenu">
                                        <li>
                                            <a href="ResponseTimes-{{ mission_id }}.html#responseTimePercentiles" onclick="$('#bodyResponseTimePercentiles').collapse('show');">
                                                Response Time Percentiles
                                            </a>
                                        </li>
                                        <li>
                                            <a href="ResponseTimes-{{ mission_id }}.html#syntheticResponseTimeDistribution" onclick="$('#bodySyntheticResponseTimeDistribution').collapse('show');">
                                                Response Time Overview
                                            </a>
                                        </li>
                                        <li>
                                            <a href="ResponseTimes-{{ mission_id }}.html#timeVsThreads" onclick="$('#bodyTimeVsThreads').collapse('show');">Time Vs Threads</a>
                                        </li>
                                        <li>
                                            <a href="ResponseTimes-{{ mission_id }}.html#responseTimeDistribution" onclick="$('#bodyResponseTimeDistribution').collapse('show');">
                                                Response Time Distribution
                                            </a>
                                        </li>
                                    </ul>

                                </li>
                            </ul>
                            <!-- /.nav-second-level -->
                        </li>

                    </ul>
                </div>
                <!-- /.sidebar-collapse -->
            </div>
            <!-- /.navbar-static-side -->
        </nav>

        <div id="page-wrapper">
            <div class="row">
                <div class="col-lg-12">
                     <div class="panel panel-default" >
                        <div class="panel-heading" style="text-align:center;">
                           <p class="dashboard-title">Test and Report informations</p>
                        </div>
                        <div class="panel-body">
                        <table id="generalInfos" class="table table-bordered table-condensed " >
                            <tr>
                                <td>File:</td>
                                <td>"LoadTest.1.jtl"</td>
                            </tr>
                            <tr>
                                <td>Start Time:</td>
                                <td>"18-8-2 下午10:05"</td>
                            </tr>
                            <tr>
                                <td>End Time:</td>
                                <td>"18-8-2 下午10:05"</td>
                            </tr>
                                <tr>
                                    <td>Filter for display:</td>
                                    <td>""</td>
                                </tr>
                        </table>
                     </div>
                </div>
            </div>
            <!-- /.row -->
            <div class="row" id="graphContainer">
                <div class="col-lg-12 portlet" id="responseTimePercentiles">
                    <div class="panel panel-default">
                        <div class="panel-heading portlet-header">
                            <i class="fa fa-bar-chart-o fa-fw"></i>  <span type="button" class="span-title dropdown-toggle click-title" data-toggle="collapse" href="#bodyResponseTimePercentiles" aria-expanded="true" aria-controls="bodyResponseTimePercentiles">Response Time Percentiles</span>
                            <div class="pull-right">
                                <div class="btn-group">
                                    <a class="drag btn btn-link btn-xs">
                                        <i class="glyphicon glyphicon-resize-vertical"></i>
                                    </a>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="dropdown">
                                        <i class="fa fa-wrench"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-user">
                                        <li><a href="#responseTimePercentiles" onClick="checkAll('choicesResponseTimePercentiles');">Display all samples</a>
                                        </li>
                                        <li><a href="#responseTimePercentiles" onClick="uncheckAll('choicesResponseTimePercentiles');">Hide all samples</a>
                                        </li>
                                        <li><a href="#responseTimePercentiles" onclick="exportToPNG('flotResponseTimesPercentiles', this);">Save as PNG</a></li>
                                    </ul>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="collapse" href="#bodyResponseTimePercentiles" aria-expanded="true" aria-controls="bodyResponseTimePercentiles">
                                        <i class="fa fa-chevron-up"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="collapse in portlet-content" id="bodyResponseTimePercentiles">
                            <div class="panel-body" id="collapseResponseTimePercentiles">
                                <div class="flot-chart">
                                    <div class="flot-chart-content" id="flotResponseTimesPercentiles" style="float: left; width:80%;"></div>
                                    <div style="float:left;margin-left:5px">
                                        <p>Zoom :</p>
                                        <div id="overviewResponseTimesPercentiles" style="width:190px;height:100px;"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="panel-footer" id="footerPercentiles">
                                <p id="legendResponseTimePercentiles" hidden></p>
                                <ul id="choicesResponseTimePercentiles" class="legend">

                                </ul>
                            </div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
                <div class="col-lg-12 portlet" id="syntheticResponseTimeDistribution">
                    <div class="panel panel-default">
                        <div class="panel-heading portlet-header">
                            <i class="fa fa-bar-chart-o fa-fw"></i>  <span type="button" class="dropdown-toggle click-title span-title" data-toggle="collapse" href="#bodySyntheticResponseTimeDistribution" aria-expanded="true" aria-controls="bodySyntheticResponseTimeDistribution">Response Time Overview</span>
                            <div class="pull-right">
                                <div class="btn-group">
                                    <a class="drag btn btn-link btn-xs">
                                        <i class="glyphicon glyphicon-resize-vertical"></i>
                                    </a>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="dropdown">
                                        <i class="fa fa-wrench"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-user">
                                        <li><a href="#syntheticResponseTimeDistribution" onClick="checkAll('choicesSyntheticResponseTimeDistribution');">Display all samples</a>
                                        </li>
                                        <li><a href="#syntheticResponseTimeDistribution" onClick="uncheckAll('choicesSyntheticRResponseTimeDistribution');">Hide all samples</a>
                                        </li>
                                        <li><a href="#syntheticResponseTimeDistribution" onclick="exportToPNG('flotSyntheticResponseTimesDistribution', this);">Save as PNG</a></li>
                                    </ul>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="collapse" href="#bodySyntheticResponseTimeDistribution" aria-expanded="true" aria-controls="bodySyntheticResponseTimeDistribution">
                                        <i class="fa fa-chevron-down"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="collapse out portlet-content" id="bodySyntheticResponseTimeDistribution">
                            <div class="panel-body" id="collapseSyntheticResponseTimeDistribution">

                                <div class="flot-chart">
                                    <div class="flot-chart-content" id="flotSyntheticResponseTimeDistribution"></div>
                                </div>
                            </div>
                            <div class="panel-footer" id="footerSyntheticResponseTimeDistribution">
                                <p id="legendSyntheticResponseTimeDistribution" hidden></p>
                                <ul id="choicesSyntheticResponseTimeDistribution" class="legend">

                                </ul>
                            </div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
                <div class="col-lg-12 portlet" id="timeVsThreads">
                    <div class="panel panel-default">
                        <div class="panel-heading portlet-header">
                           <i class="fa fa-bar-chart-o fa-fw"></i><span type="button" class="span-title dropdown-toggle click-title" data-toggle="collapse" href="#bodyTimeVsThreads" aria-expanded="true" aria-controls="bodyTimeVsThreads">Time Vs Threads</span>
                           <div class="pull-right">
                                <div class="btn-group">
                                    <a class="drag btn btn-link btn-xs">
                                        <i class="glyphicon glyphicon-resize-vertical"></i>
                                    </a>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="dropdown">
                                        <i class="fa fa-wrench"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-user">
                                        <li><a href="#timeVsThreads" onClick="checkAll('choicesTimeVsThreads');">Display all samples</a>
                                        </li>
                                        <li><a href="#timeVsThreads" onClick="uncheckAll('choicesTimeVsThreads');">Hide all samples</a>
                                        </li>
                                        <li><a href="#timeVsThreads" onclick="exportToPNG('flotTimesVsThreads', this);">Save as PNG</a></li>
                                    </ul>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="collapse" href="#bodyTimeVsThreads" aria-expanded="true" aria-controls="bodyTimeVsThreads">
                                        <i class="fa fa-chevron-down"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="collapse out portlet-content" id="bodyTimeVsThreads">
                            <div class="panel-body" id="collapseTimeVsThreads">
                                <div class="flot-chart">
                                    <div class="flot-chart-content" id="flotTimesVsThreads" style="float: left; width:80%;"></div>
                                    <div style="float:left;margin-left:5px">
                                        <p>Zoom :</p>
                                        <div id="overviewTimesVsThreads" style="width:190px;height:100px;"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="panel-footer" id="footerTimeVsThreads">
                                <p id="legendTimeVsThreads" hidden></p>
                                <ul id="choicesTimeVsThreads" class="legend"></ul>
                            </div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
                <div class="col-lg-12 portlet" id="responseTimeDistribution">
                    <div class="panel panel-default">
                        <div class="panel-heading portlet-header">
                           <i class="fa fa-bar-chart-o fa-fw"></i> <span type="button" class="dropdown-toggle click-title span-title" data-toggle="collapse" href="#bodyResponseTimeDistribution" aria-expanded="true" aria-controls="bodyResponseTimeDistribution">Response Time Distribution</span>
                           <div class="pull-right">
                                <div class="btn-group">
                                    <a class="drag btn btn-link btn-xs">
                                        <i class="glyphicon glyphicon-resize-vertical"></i>
                                    </a>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="dropdown">
                                        <i class="fa fa-wrench"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-user">
                                        <li><a href="#responseTimeDistribution" onClick="checkAll('choicesResponseTimeDistribution');">Display all samples</a>
                                        </li>
                                        <li><a href="#responseTimeDistribution" onClick="uncheckAll('choicesResponseTimeDistribution');">Hide all samples</a>
                                        </li>
                                        <li><a href="#responseTimeDistribution" onclick="exportToPNG('flotResponseTimeDistribution', this);">Save as PNG</a></li>
                                    </ul>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="collapse" href="#bodyResponseTimeDistribution" aria-expanded="true" aria-controls="bodyResponseTimeDistribution">
                                        <i class="fa fa-chevron-down"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="collapse out portlet-content" id="bodyResponseTimeDistribution">
                            <div class="panel-body" id="collapseResponseTimeDistribution">

                                <div class="flot-chart">
                                    <div class="flot-chart-content" id="flotResponseTimeDistribution"></div>
                                </div>
                            </div>
                            <div class="panel-footer" id="footerResponseTimeDistribution">
                                <p id="legendResponseTimeDistribution" hidden></p>
                                <ul id="choicesResponseTimeDistribution" class="legend">

                                </ul>
                            </div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>

                <!-- /.col-lg-6 -->
            </div>
            <!-- /.row -->
        </div>
        <!-- /#page-wrapper -->
    </div>
    <!-- /#wrapper -->
     <!-- jQuery -->
    <script src="../../sbadmin2-1.0.7/bower_components/jquery/dist/jquery.min.js"></script>
    <!-- Bootstrap Core JavaScript -->
    <script src="../../sbadmin2-1.0.7/bower_components/bootstrap/dist/js/bootstrap.min.js"></script>
    <!-- Metis Menu Plugin JavaScript -->
    <script src="../../sbadmin2-1.0.7/bower_components/metisMenu/dist/metisMenu.min.js"></script>
    <!-- Flot Charts JavaScript -->
    <script src="../../sbadmin2-1.0.7/bower_components/flot/excanvas.min.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.pie.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.resize.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.canvas.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.navigate.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.time.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.selection.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot.tooltip/js/jquery.flot.tooltip.min.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot-axislabels/jquery.flot.axislabels.js"></script>
    <script src="../js/hashtable.js"></script>
    <script src="../js/jquery.numberformatter-1.2.3.min.js"></script>
    <script src="../js/curvedLines.js"></script>
    <script src="../js/dashboard-commons.js"></script>
    <script src="../js/graph-{{ mission_id }}.js"></script>
    <script src="../js/jquery-ui.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.threshold.js"></script>
    <!-- Custom Theme JavaScript -->
    <script src="../../sbadmin2-1.0.7/dist/js/sb-admin-2.js"></script>
    <script src="../js/jquery.cookie.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.symbol.js"></script>
</body>
</html>
""",
    "Throughput": """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Apache JMeter Dashboard</title>

    <!-- Bootstrap Core CSS -->
    <link href="../../sbadmin2-1.0.7/bower_components/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- icon -->
    <link rel="icon" type="image/png" href="icon-apache.png" />

    <!-- MetisMenu CSS -->
    <link href="../../sbadmin2-1.0.7/bower_components/metisMenu/dist/metisMenu.min.css" rel="stylesheet">

    <!-- Legends CSS -->
    <link href="../css/legends.css" rel="stylesheet">


    <!-- Custom CSS -->
    <link href="../../sbadmin2-1.0.7/dist/css/sb-admin-2.css" rel="stylesheet">

    <!-- Custom Fonts -->
    <link href="../../sbadmin2-1.0.7/bower_components/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">

   <!-- JQuery UI style -->
    <link href="../css/jquery-ui.css" rel="stylesheet">
    <link href="../css/jquery-ui.structure.css" rel="stylesheet">
    <link href="../css/jquery-ui.theme.css" rel="stylesheet">
</head>

<body>

    <div id="wrapper">

        <!-- Navigation -->
        <nav class="navbar navbar-default navbar-static-top" role="navigation" style="margin-bottom: 0">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="../../index-{{ mission_id }}.html">Apache JMeter Dashboard</a>
            </div>
            <!-- /.navbar-header -->


            <div class="navbar-default sidebar" role="navigation">
                <div class="sidebar-nav navbar-collapse">
                    <ul class="nav" id="side-menu">

                        <li>
                            <a href="../../index-{{ mission_id }}.html"><i class="fa fa-dashboard fa-fw"></i> Dashboard</a>
                        </li>
                        <li>
                            <a href="#"><i class="fa fa-bar-chart-o fa-fw"></i> Charts<span class="fa arrow"></span></a>
                            <ul class="nav nav-second-level">
                                <li>
                                    <a href="OverTime-{{ mission_id }}.html">Over Time</a>
                                </li>
                                <li>
                                    <a href="Throughput-{{ mission_id }}.html">Throughput<span class="fa arrow"></span></a>
                                    <ul class="nav nav-third-level in" id="submenu">
                                        <li>
                                            <a href="Throughput-{{ mission_id }}.html#hitsPerSecond" onclick="$('#bodyHitsPerSecond').collapse('show');">Hits Per Second</a>
                                        </li>

                                        <li>
                                            <a href="Throughput-{{ mission_id }}.html#codesPerSecond" onclick="$('#bodyCodesPerSecond').collapse('show');">Codes Per Second</a>
                                        </li>
                                        <li>
                                            <a href="Throughput-{{ mission_id }}.html#transactionsPerSecond" onclick="$('#bodyTransactionsPerSecond').collapse('show');">Transactions Per Second</a>
                                        </li>
                                        <li>
                                            <a href="Throughput-{{ mission_id }}.html#responseTimeVsRequest" onclick="$('#bodyResponseTimeVsRequest').collapse('show');">Response Time Vs Request</a>
                                        </li>
                                        <li>
                                            <a href="Throughput-{{ mission_id }}.html#latencyVsRequest" onclick="$('#bodyLatenciesVsRequest').collapse('show');">Latency Vs Request</a>
                                        </li>
                                    </ul>
                                </li>
                                <li>
                                    <a href="ResponseTimes-{{ mission_id }}.html">Response Times</a>
                                </li>
                            </ul>
                            <!-- /.nav-second-level -->
                        </li>

                    </ul>
                </div>
                <!-- /.sidebar-collapse -->
            </div>
            <!-- /.navbar-static-side -->
        </nav>

        <div id="page-wrapper">
            <div class="row">
                <div class="col-lg-12">
                     <div class="panel panel-default">
                        <div class="panel-heading" style="text-align:center;">
                           <p class="dashboard-title">Test and Report informations</p>
                        </div>
                        <div class="panel-body">
                        <table id="generalInfos" class="table table-bordered table-condensed " >
                            <tr>
                                <td>File:</td>
                                <td>"LoadTest.1.jtl"</td>
                            </tr>
                            <tr>
                                <td>Start Time:</td>
                                <td>"18-8-2 下午10:05"</td>
                            </tr>
                            <tr>
                                <td>End Time:</td>
                                <td>"18-8-2 下午10:05"</td>
                            </tr>
                                <tr>
                                    <td>Filter for display:</td>
                                    <td>""</td>
                                </tr>
                        </table>
                     </div>
                </div>
            </div>
            <!-- /.row -->
            <div class="row" id="graphContainer">

                <!-- /.col-lg-12 -->

                <div class="col-lg-12 portlet" id="hitsPerSecond">
                    <div class="panel panel-default">
                        <div class="panel-heading portlet-header">
                           <i class="fa fa-bar-chart-o fa-fw"> </i>  <span type="button" class="dropdown-toggle click-title span-title" data-toggle="collapse" href="#bodyHitsPerSecond" aria-expanded="true" aria-controls="bodyHitsPerSecond">Hits Per Second (excluding embedded resources)</span>
                           <div class="pull-right">
                                <div class="btn-group">
                                    <a class="btn btn-link btn-xs">
                                        <i class="glyphicon glyphicon-resize-vertical"></i>
                                    </a>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="dropdown">
                                        <i class="fa fa-wrench"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-user">
                                        <li><a href="#hitsPerSecond" onClick="checkAll('choicesHitsPerSecond');">Display samples</a>
                                        </li>
                                        <li><a href="#hitsPerSecond" onClick="uncheckAll('choicesHitsPerSecond');">Hide samples</a>
                                        </li>
                                        <li><a href="#hitsPerSecond" onclick="exportToPNG('flotHitsPerSecond', this);">Save as PNG</a></li>
                                    </ul>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="collapse" href="#bodyHitsPerSecond" aria-expanded="true" aria-controls="bodyHitsPerSecond">
                                        <i class="fa fa-chevron-up"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="collapse in portlet-content" id="bodyHitsPerSecond">
                            <div class="panel-body" id="collapseHitsPerSecond" >
                                <div class="flot-chart" >
                                    <div class="flot-chart-content" id="flotHitsPerSecond" style="float: left; width:80%;"></div>
                                    <div style="float:left;margin-left:5px">
                                        <p>Zoom :</p>
                                        <div id="overviewHitsPerSecond" style="width:190px;height:100px;"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="panel-footer" id="footerHitsPerSecond">
                                <p id="legendHitsPerSecond" hidden></p>
                                <ul id="choicesHitsPerSecond" class="legend"></ul>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- codesPerSecond -->

                <div class="col-lg-12 portlet" id="codesPerSecond">
                    <div class="panel panel-default">
                        <div class="panel-heading portlet-header">
                            <i class="fa fa-bar-chart-o fa-fw"></i>
                            <span type="button" class="dropdown-toggle click-title span-title" data-toggle="collapse" href="#bodyCodesPerSecond" aria-expanded="true" aria-controls="bodyCodesPerSecond">Codes Per Second (excluding embedded resources)</span>
                            <div class="pull-right">
                                <div class="btn-group">
                                    <a class="btn btn-link btn-xs">
                                        <i class="glyphicon glyphicon-resize-vertical"></i>
                                    </a>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="dropdown">
                                        <i class="fa fa-wrench"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-user">
                                        <li><a href="#codesPerSecond" onClick="checkAll('choicesCodesPerSecond');">Display samples</a>
                                        </li>
                                        <li><a href="#codesPerSecond" onClick="uncheckAll('choicesCodesPerSecond');">Hide samples</a>
                                        </li>
                                        <li><a href="#codesPerSecond" onclick="exportToPNG('flotCodesPerSecond', this);">Save as PNG</a></li>
                                    </ul>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="collapse" href="#bodyCodesPerSecond" aria-expanded="true" aria-controls="bodyCodesPerSecond">
                                        <i class="fa fa-chevron-down"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->

                        <div class="collapse out portlet-content" id="bodyCodesPerSecond">
                            <div class="panel-body" id="collapseCodesPerSecond">
                                <div class="flot-chart">
                                    <div class="flot-chart-content" id="flotCodesPerSecond" style="float: left; width:80%;"></div>
                                    <div style="float:left;margin-left:5px">
                                        <p>Zoom :</p>
                                        <div id="overviewCodesPerSecond" style="width:190px;height:100px;"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="panel-footer" id="footerCodesPerSecond">
                                <p id="legendCodesPerSecond" hidden></p>
                                <ul id="choicesCodesPerSecond" class="legend"></ul>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-lg-12 portlet" id="transactionsPerSecond">
                    <div class="panel panel-default">
                        <div class="panel-heading portlet-header">
                          <i class="fa fa-bar-chart-o fa-fw"> </i> <span type="button" class="dropdown-toggle click-title span-title" data-toggle="collapse" href="#bodyTransactionsPerSecond" aria-expanded="true" aria-controls="bodyTransactionsPerSecond">Transactions Per Second</span>
                          <div class="pull-right">
                                <div class="btn-group">
                                    <a class="btn btn-link btn-xs">
                                        <i class="glyphicon glyphicon-resize-vertical"></i>
                                    </a>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="dropdown">
                                        <i class="fa fa-wrench"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-user">
                                        <li><a href="#transactionsPerSecond" onClick="checkAll('choicesTransactionsPerSecond');">Display all samples</a>
                                        </li>
                                        <li><a href="#transactionsPerSecond" onClick="uncheckAll('choicesTransactionsPerSecond');">Hide all samples</a>
                                        </li>
                                        <li><a href="#transactionsPerSecond" onclick="exportToPNG('flotTransactionsPerSecond', this);">Save as PNG</a></li>
                                    </ul>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="collapse" href="#bodyTransactionsPerSecond" aria-expanded="true" aria-controls="bodyTransactionsPerSecond">
                                        <i class="fa fa-chevron-down"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="collapse out portlet-content" id="bodyTransactionsPerSecond">
                            <div class="panel-body" id="collapseTransactionsPerSecond">
                                <div class="flot-chart">
                                    <div class="flot-chart-content" id="flotTransactionsPerSecond" style="float: left; width:80%;"></div>
                                    <div style="float:left;margin-left:5px">
                                        <p>Zoom :</p>
                                        <div id="overviewTransactionsPerSecond" style="width:190px;height:100px;"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="panel-footer" id="footerTransactionsPerSecond">
                                <p id="legendTransactionsPerSecond" hidden></p>
                                <ul id="choicesTransactionsPerSecond" class="legend"></ul>
                            </div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>

                <div class="col-lg-12 portlet" id="responseTimeVsRequest">
                    <div class="panel panel-default">
                        <div class="panel-heading portlet-header">
                          <i class="fa fa-bar-chart-o fa-fw"> </i> <span type="button" class="dropdown-toggle click-title span-title" data-toggle="collapse" href="#bodyResponseTimeVsRequest" aria-expanded="true" aria-controls="bodyResponseTimeVsRequest">Response Time Vs Request</span>
                          <div class="pull-right">
                                <div class="btn-group">
                                    <a class="btn btn-link btn-xs">
                                        <i class="glyphicon glyphicon-resize-vertical"></i>
                                    </a>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="dropdown">
                                        <i class="fa fa-wrench"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-user">
                                        <li><a href="#responseTimeVsRequest" onClick="checkAll('choicesResponseTimeVsRequest');">Display all samples</a>
                                        </li>
                                        <li><a href="#responseTimeVsRequest" onClick="uncheckAll('choicesResponseTimeVsRequest');">Hide all samples</a>
                                        </li>
                                        <li><a href="#responseTimeVsRequest" onclick="exportToPNG('flotResponseTimeVsRequest', this);">Save as PNG</a></li>
                                    </ul>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="collapse" href="#bodyResponseTimeVsRequest" aria-expanded="true" aria-controls="bodyResponseTimeVsRequest">
                                        <i class="fa fa-chevron-down"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="collapse out portlet-content" id="bodyResponseTimeVsRequest">
                            <div class="panel-body" id="collapseResponseTimeVsRequest">
                                <div class="flot-chart">
                                    <div class="flot-chart-content" id="flotResponseTimeVsRequest" style="float: left; width:80%;"></div>
                                    <div style="float:left;margin-left:5px">
                                        <p>Zoom :</p>
                                        <div id="overviewResponseTimeVsRequest" style="width:190px;height:100px;"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="panel-footer" id="footerResponseRimeVsRequest">
                                    <p id="legendResponseTimeVsRequest" hidden></p>
                                    <ul id="choicesResponseTimeVsRequest" class="legend"></ul>
                            </div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
               <div class="col-lg-12 portlet" id="latencyVsRequest">
                    <div class="panel panel-default">
                        <div class="panel-heading portlet-header">
                          <i class="fa fa-bar-chart-o fa-fw"> </i> <span type="button" class="dropdown-toggle click-title span-title" data-toggle="collapse" href="#bodyLatenciesVsRequest" aria-expanded="true" aria-controls="bodyLatenciesVsRequest">Latency Vs Request</span>
                          <div class="pull-right">
                                <div class="btn-group">
                                    <a class="btn btn-link btn-xs">
                                        <i class="glyphicon glyphicon-resize-vertical"></i>
                                    </a>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="dropdown">
                                        <i class="fa fa-wrench"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-user">
                                        <li><a href="#latencyVsRequest" onClick="checkAll('choicesLatencyVsRequest');">Display all samples</a>
                                        </li>
                                        <li><a href="#latencyVsRequest" onClick="uncheckAll('choicesLatencyVsRequest');">Hide all samples</a>
                                        </li>
                                        <li><a href="#latencyVsRequest" onclick="exportToPNG('flotLatenciesVsRequest', this);">Save as PNG</a></li>
                                    </ul>
                                    <button type="button" class="btn btn-link btn-xs dropdown-toggle" data-toggle="collapse" href="#bodyLatenciesVsRequest" aria-expanded="true" aria-controls="bodyLatenciesVsRequest">
                                        <i class="fa fa-chevron-down"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-heading -->
                        <div class="collapse out portlet-content" id="bodyLatenciesVsRequest">
                            <div class="panel-body" id="collapseLatencyVsRequest">
                                <div class="flot-chart">
                                    <div class="flot-chart-content" id="flotLatenciesVsRequest" style="float: left; width:80%;"></div>
                                    <div style="float:left;margin-left:5px">
                                        <p>Zoom :</p>
                                        <div id="overviewLatenciesVsRequest" style="width:190px;height:100px;"></div>
                                    </div>
                                </div>
                                <div class="panel-footer" id="footerLatenciesVsRequest">
                                    <p id="legendLatencyVsRequest" hidden></p>
                                    <ul id="choicesLatencyVsRequest" class="legend"></ul>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
            </div>
            <!-- /.row -->
        </div>
        <!-- /#page-wrapper -->
    </div>
    <!-- /#wrapper -->
     <!-- jQuery -->
    <script src="../../sbadmin2-1.0.7/bower_components/jquery/dist/jquery.min.js"></script>
    <!-- Bootstrap Core JavaScript -->
    <script src="../../sbadmin2-1.0.7/bower_components/bootstrap/dist/js/bootstrap.min.js"></script>
    <!-- Metis Menu Plugin JavaScript -->
    <script src="../../sbadmin2-1.0.7/bower_components/metisMenu/dist/metisMenu.min.js"></script>
    <!-- Flot Charts JavaScript -->
    <script src="../../sbadmin2-1.0.7/bower_components/flot/excanvas.min.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.pie.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.resize.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.canvas.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.time.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot/jquery.flot.selection.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot.tooltip/js/jquery.flot.tooltip.min.js"></script>
    <script src="../../sbadmin2-1.0.7/bower_components/flot-axislabels/jquery.flot.axislabels.js"></script>
    <script src="../js/hashtable.js"></script>
    <script src="../js/jquery.numberformatter-1.2.3.min.js"></script>
    <script src="../js/curvedLines.js"></script>
    <script src="../js/dashboard-commons.js"></script>
    <script src="../js/graph-{{ mission_id }}.js"></script>
    <script src="../js/jquery-ui.js"></script>
    <!-- Custom Theme JavaScript -->
    <script src="../../sbadmin2-1.0.7/dist/js/sb-admin-2.js"></script>
    <script src="../js/jquery.cookie.js"></script>
</body>
</html>
"""
}
