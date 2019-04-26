# -*- encoding:utf-8 -*-

jmeter_template = """
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="3.2" jmeter="3.3 r1808647">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="{{ missionName }}" enabled="true">
      <stringProp name="TestPlan.comments"></stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">{% if gradient %}true{% else %}false{% endif %}</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="用户定义的变量" enabled="true">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <stringProp name="TestPlan.user_define_classpath"></stringProp>
    </TestPlan>
    <hashTree>
    {% for tg in gradient %}
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="performance_script_template" enabled="true">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="循环控制器" enabled="true">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">{% if scheduleron == "true" %}-1{% else %}{{ loopcount }}{% endif %}</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">{% if tg|int >= enable_distributed_concurrent and agent_count != 0 %}{{ agent_concurrent }}{% else %}{{ tg }}{% endif %}</stringProp>
        <stringProp name="ThreadGroup.ramp_time">{{ ramptime }}</stringProp>
        <longProp name="ThreadGroup.start_time">1389388830000</longProp>
        <longProp name="ThreadGroup.end_time">1389388830000</longProp>
        <boolProp name="ThreadGroup.scheduler">{{ scheduleron }}</boolProp>
        <stringProp name="ThreadGroup.duration">{{ loopcount }}</stringProp>
        <stringProp name="ThreadGroup.delay"></stringProp>
      </ThreadGroup>
      <hashTree>
        {% for api in apis %}
            {% if api.file %}
            <CSVDataSet guiclass="TestBeanGUI" testclass="CSVDataSet" testname="CSV Data Set Config" enabled="true">
              <stringProp name="delimiter">{{ api.delimiter }}</stringProp>
              <stringProp name="fileEncoding">UTF-8</stringProp>
              <stringProp name="filename">{{ upload_folder }}/{{ user }}_{{ api.file[0] }}</stringProp>
              <boolProp name="ignoreFirstLine">false</boolProp>
              <boolProp name="quotedData">false</boolProp>
              <boolProp name="recycle">true</boolProp>
              <stringProp name="shareMode">shareMode.all</stringProp>
              <boolProp name="stopThread">false</boolProp>
              <stringProp name="variableNames">{{ api.file[1] }}</stringProp>
            </CSVDataSet>
            <hashTree/>
            {% endif %}
            <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="接口_{{ loop.index }} - 并发:{{ tg }}" enabled="true">
            {% if api.body %}
              <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
              <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
                <collectionProp name="Arguments.arguments">
                  <elementProp name="" elementType="HTTPArgument">
                    <boolProp name="HTTPArgument.always_encode">false</boolProp>
                    <stringProp name="Argument.value">{{ api.body }}</stringProp>
                    <stringProp name="Argument.metadata">=</stringProp>
                  </elementProp>
                </collectionProp>
              </elementProp>
            {% endif %}
              <stringProp name="HTTPSampler.domain">{{ host }}</stringProp>
              <stringProp name="HTTPSampler.port">{{ port }}</stringProp>
              <stringProp name="HTTPSampler.protocol">http</stringProp>
              <stringProp name="HTTPSampler.contentEncoding">utf-8</stringProp>
              <stringProp name="HTTPSampler.path">{{ api.path|replace("&", "&amp;") }}</stringProp>
              <stringProp name="HTTPSampler.method">{{ api.method|upper }}</stringProp>
              <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
              <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
              <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
              <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
              <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
              <stringProp name="HTTPSampler.connect_timeout">{% if api.check_resptime %}{{ api.check_resptime }}{% endif %}</stringProp>
              <stringProp name="HTTPSampler.response_timeout">{% if api.check_resptime %}{{ api.check_resptime }}{% endif %}</stringProp>
            </HTTPSamplerProxy>
            <hashTree>
                <ResultCollector guiclass="ViewResultsFullVisualizer" testclass="ResultCollector" testname="detaillog" enabled="true">
                  <boolProp name="ResultCollector.error_logging">true</boolProp>
                  <objProp>
                    <name>saveConfig</name>
                    <value class="SampleSaveConfiguration">
                      <time>true</time>
                      <latency>false</latency>
                      <timestamp>false</timestamp>
                      <success>false</success>
                      <label>false</label>
                      <code>true</code>
                      <message>true</message>
                      <threadName>false</threadName>
                      <dataType>false</dataType>
                      <encoding>false</encoding>
                      <assertions>false</assertions>
                      <subresults>true</subresults>
                      <responseData>true</responseData>
                      <samplerData>true</samplerData>
                      <xml>false</xml>
                      <fieldNames>true</fieldNames>
                      <responseHeaders>false</responseHeaders>
                      <requestHeaders>false</requestHeaders>
                      <responseDataOnError>true</responseDataOnError>
                      <saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage>
                      <assertionsResultsToSave>0</assertionsResultsToSave>
                      <url>true</url>
                      <connectTime>true</connectTime>
                    </value>
                  </objProp>
                  <stringProp name="filename">{{ debug_detail_folder }}/{{ user }}_{{ mission_id }}_接口_{{ loop.index }}_error.txt</stringProp>
                </ResultCollector>
                <hashTree/>
                {% if api.jmeter_header %}
                <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="HTTP信息头管理器" enabled="true">
                    <collectionProp name="HeaderManager.headers">
                    {% for key, value in api.jmeter_header.iteritems() %}
                        <elementProp name="" elementType="Header">
                            <stringProp name="Header.name">{{ key }}</stringProp>
                            <stringProp name="Header.value">{{ value }}</stringProp>
                        </elementProp>
                    {% endfor %}
                    </collectionProp>
                </HeaderManager>
                <hashTree/>
                {% endif %}
                {% if api.check_code %}
                <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="响应断言" enabled="true">
                    <collectionProp name="Asserion.test_strings">
                      <stringProp name="49586">{{ api.check_code }}</stringProp>
                    </collectionProp>
                    <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
                    <boolProp name="Assertion.assume_success">false</boolProp>
                    <intProp name="Assertion.test_type">8</intProp>
                </ResponseAssertion>
                <hashTree/>
                {% endif %}
                {% if api.check_body %}
                <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="响应断言" enabled="true">
                    <collectionProp name="Asserion.test_strings">
                    <stringProp name="-869514794">{{ api.check_body }}</stringProp>
                    </collectionProp>
                    <stringProp name="Assertion.test_field">Assertion.response_data</stringProp>
                    <boolProp name="Assertion.assume_success">false</boolProp>
                    <intProp name="Assertion.test_type">2</intProp>
                </ResponseAssertion>
                <hashTree/>
                {% endif %}
                {% if api.thinktime %}
                <ConstantTimer guiclass="ConstantTimerGui" testclass="ConstantTimer" testname="固定定时器" enabled="true">
                    <stringProp name="ConstantTimer.delay">{{ api.thinktime|float *1000|int }}</stringProp>
                </ConstantTimer>
                <hashTree/>
                {% endif %}
                {% if api.envs %}
                {% for env in api.envs %}
                    {% if env["extracttype"] == "jsonPath" %}
                        <JSONPostProcessor guiclass="JSONPostProcessorGui" testclass="JSONPostProcessor" testname="JSON Extractor" enabled="true">
                            <stringProp name="JSONPostProcessor.referenceNames">{{ env["name"] }}</stringProp>
                            <stringProp name="JSONPostProcessor.jsonPathExprs">{{ env["expression"] }}</stringProp>
                            <stringProp name="JSONPostProcessor.match_numbers"></stringProp>
                        </JSONPostProcessor>
                        <hashTree/>
                    {% else %}
                        <RegexExtractor guiclass="RegexExtractorGui" testclass="RegexExtractor" testname="正则表达式提取器" enabled="true">
                            <stringProp name="RegexExtractor.useHeaders">{% if env["source"] == "header" %}true{% else %}false{% endif %}</stringProp>
                            <stringProp name="RegexExtractor.refname">{{ env["name"] }}</stringProp>
                            <stringProp name="RegexExtractor.regex">{{ env["expression"] }}</stringProp>
                            <stringProp name="RegexExtractor.template">$1$</stringProp>
                            <stringProp name="RegexExtractor.default"></stringProp>
                            <stringProp name="RegexExtractor.match_number"></stringProp>
                        </RegexExtractor>
                        <hashTree/>
                    {% endif %}
                {% endfor %}
                {% endif %}
            </hashTree>
        {% endfor %}
      </hashTree>
      {% endfor %}
    </hashTree>
    <WorkBench guiclass="WorkBenchGui" testclass="WorkBench" testname="工作台" enabled="true">
      <boolProp name="WorkBench.save">true</boolProp>
    </WorkBench>
    <hashTree/>
  </hashTree>
</jmeterTestPlan>
"""

gatling_template = """package {{ user }}

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class {{ className }} extends Simulation {

    var httpConfig = http.baseURL("{{ baseUrl }}").doNotTrackHeader("1")
    {% for tg in gradient %}
    object ApiFlow_{{ loop.index }} {
        {% for api in apis %}
        {% if api.file %}var feeder_{{ api.name }} = csv("{{ user }}_{{ api.file }}").random{% endif %}{% endfor %}
        var flow ={% for api in apis %} {% if api.file %}{% if not loop.first %}.{% endif %}feed(feeder_{{api.name}}){% endif %}{% if api.file %}.{% elif not loop.first %}.{% else %}{% endif %}exec(http("{{ api.name }} 并发:{{ tg }}")
            .{{ api.method }}("{{ api.path }}")
            {% if api.gatling_header %}.headers({{ api.gatling_header }}){% endif %}
            {% if api.body %}.body(StringBody(\"\"\"{{ api.body }}\"\"\")).asJSON{% endif %}
            {% if api.check_code %}.check(status.is({{ api.check_code }})){% endif %}
            {% if api.check_body %}.check(regex(\"\"\"{{ api.check_body }}\"\"\").exists){% endif %}
            {% if api.check_resptime %}.check(responseTimeInMillis.lessThan({{ api.check_resptime }})){% endif %}
            {% if api.envs %}
        {% for env in api.envs %}
            {% if env["source"] == "header" %}
                .check(header("{{ env['expression'] }}").saveAs("{{ env['name'] }}"))
            {% else %}
                .check({% if env["extracttype"] == "regex" %}regex(\"\"\"{{ env['expression'] }}\"\"\"){% else %}jsonPath("{{ env['expression'] }}"){% endif %}.saveAs("{{ env['name'] }}"))
            {% endif %}
        {% endfor %}
            {% endif %}
            )
            {% if api.thinktime %}
            .pause({{ api.thinktime }} seconds)
            {% endif %}
        {% endfor %}
    }

    var scn_{{ loop.index }} = scenario("concurrent_{{ tg }}").exec(
        ApiFlow_{{ loop.index }}.flow
    )
    {% endfor %}

    setUp(
        {% for tg in gradient %}
        scn_{{ loop.index }}.inject(
            nothingFor({{ duration * loop.index0 + 1 * loop.index0 }} {{ durationType}}),
            {% if loadtype == "atOnceUsers" %}
                atOnceUsers({{ tg }})       //一次模拟的用户数量(nbUsers)
            {% elif loadtype == "rampUsers" %}
                rampUsers({{ tg }}) over({{ duration }} {{ durationType }})   //在指定的时间段内逐渐增加用户数到指定的数量(nbUsers)。
            {% elif loadtype == "constantUsersPerSec" %}
                constantUsersPerSec({{ tg }}) during({{ duration }} {{ durationType }})   //以固定的速度模拟用户，指定每秒模拟的用户数(rate)，指定模拟测试时间长度(duration)。
            {% elif loadtype == "rampUsersPerSec" %}
                rampUsersPerSec({{ tg }}) to({{ concurrent2 }}) during({{ duration }} {{ durationType }})  //在指定的时间(duration)内，使每秒模拟的用户从数量1(rate1)逐渐增加到数量2(rate2)，速度匀速
            {% elif loadtype == "heavisideUsers" %}
                heavisideUsers({{ tg }}) over({{ duration }} {{ durationType }})   //每秒并发用户数递增。
            {% else %}
                atOnceUsers({{ tg }})   //一次模拟的用户数量(nbUsers)
            {% endif %}
        ).protocols(httpConfig){% if not loop.last%},{% endif %}
        {% endfor %}
    )
}
"""