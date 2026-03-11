// widget-render.js - 공통 위젯 렌더링
const LABELS = {
    'kpi_total_hosp':'전체 병원','kpi_active_hosp':'운영 병원','kpi_total_kiosk':'전체 키오스크',
    'kpi_today_count':'오늘 이용건수','kpi_today_hosp':'오늘 이용병원','kpi_today_kiosk':'오늘 이용키오스크',
    'kpi_online_agent':'온라인 에이전트','kpi_error_agent':'장애 키오스크','kpi_total_agent':'전체 에이전트',
    'kpi_offline_agent':'오프라인 에이전트','kpi_open_alarms':'미처리 알람','kpi_open_tickets':'미처리 티켓',
    'kpi_today_alarm':'오늘 장애건수','kpi_avg_response':'평균 응답시간','kpi_month_count':'이번달 누적',
    'kpi_equipment_alert':'장비 이상 현황',
    'isv_list':'ISV 파트너','recent_usage':'최근 사용현황','alarm_list':'최근 알람',
    'ticket_list':'최근 티켓','agent_status':'에이전트 상태','weekly_chart':'주간 이용 추이',
    'isv_chart':'ISV 분포','chart_monthly':'월별 이용 추이','chart_hourly':'시간대별 이용현황',
    'chart_isv_today':'ISV별 오늘 이용','table_error_kiosks':'장애 키오스크',
    'table_no_heartbeat':'미응답 키오스크','table_top10_today':'오늘 이용 TOP10',
    'chart_daily_trend':'일별 이용 추이','chart_daily_hosp':'일별 병원 추이',
    'table_snapshot_top':'스냅샷 TOP','clock':'시계','text_block':'텍스트'
};

const CHART_COLORS = ['#00d4ff','#00ff88','#a855f7','#ff4444','#ffaa00','#ff6b6b','#4ecdc4','#45b7d1','#96ceb4','#ffeaa7','#74b9ff','#fd79a8'];

function _kpiHtml(el, val, color, type) {
    const bw=el.offsetWidth, bh=el.offsetHeight;
    const numFs=Math.max(20,Math.min(72,Math.min(bw/3.5,bh/2)));
    return '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;padding:4px">'
        +'<div class="kpi-val" style="font-size:'+numFs+'px;font-weight:bold;color:'+color+';line-height:1.1">'+val+'</div></div>';
}

function _makeChart(body, id, cfg) {
    const cid = 'chart_'+(id||Math.random().toString(36).slice(2));
    body.innerHTML='<canvas id="'+cid+'" style="width:100%;height:100%"></canvas>';
    setTimeout(()=>{
        const ctx=document.getElementById(cid);
        if(ctx) new Chart(ctx, cfg);
    },100);
    return cid;
}

function _chartScales(opts){
    return Object.assign({
        x:{ticks:{color:'#fff',font:{size:12},autoSkip:true,maxTicksLimit:10,maxRotation:45},grid:{display:false},display:true},
        y:{ticks:{color:'#fff',font:{size:12}},grid:{display:false},display:true}
    }, opts||{});
}

async function renderWidgetContent(el, body, type, id) {
    const label = LABELS[type]||type;
    try {
    // ===== KPI: 기본 6종 =====
    if(type==='kpi_total_hosp'||type==='kpi_active_hosp'||type==='kpi_total_kiosk'){
        const d=await(await fetch('/api/widget-data/kpi_summary')).json();
        let val=type==='kpi_total_hosp'?d.total_hosp:type==='kpi_active_hosp'?d.active_hosp:d.total_kiosk;
        let color=type==='kpi_active_hosp'?'#2ed573':'#4ecdc4';
        body.innerHTML=_kpiHtml(el,val,color,type);
    }
    else if(type==='kpi_today_count'||type==='kpi_today_hosp'||type==='kpi_today_kiosk'){
        const d=await(await fetch('/api/widget-data/today_usage')).json();
        let val=type==='kpi_today_count'?d.total_count:type==='kpi_today_hosp'?d.hosp_count:d.kiosk_count;
        let color=type==='kpi_today_count'?'#feca57':type==='kpi_today_hosp'?'#ff9ff3':'#54a0ff';
        body.innerHTML=_kpiHtml(el,Number(val).toLocaleString(),color,type);
    }
    // ===== KPI: 에이전트 =====
    else if(type==='kpi_online_agent'||type==='kpi_error_agent'||type==='kpi_total_agent'||type==='kpi_offline_agent'){
        const d=await(await fetch('/api/widget-data/agent_summary')).json();
        let val,color;
        if(type==='kpi_online_agent'){val=d.online;color='#2ed573';}
        else if(type==='kpi_error_agent'){val=d.error||0;color='#ff4757';}
        else if(type==='kpi_total_agent'){val=d.total;color='#4ecdc4';}
        else{val=d.offline||0;color='#888';}
        body.innerHTML=_kpiHtml(el,val,color,type);
    }
    // ===== KPI: 알람/티켓 =====
    else if(type==='kpi_open_alarms'){
        const d=await(await fetch('/api/widget-data/alarm_summary')).json();
        body.innerHTML=_kpiHtml(el,d.open,'#ff6b6b',type);
    }
    else if(type==='kpi_open_tickets'){
        const d=await(await fetch('/api/widget-data/ticket_summary')).json();
        body.innerHTML=_kpiHtml(el,d.open,'#feca57',type);
    }
    // ===== KPI: 신규 3종 =====
    else if(type==='kpi_today_alarm'){
        const d=await(await fetch('/api/widget-data/today_alarm')).json();
        body.innerHTML=_kpiHtml(el,d.count,'#ff6b6b',type);
    }
    else if(type==='kpi_avg_response'){
        const d=await(await fetch('/api/widget-data/avg_response')).json();
        const c=d.avg_ms<200?'#00ff88':d.avg_ms<500?'#ffaa00':'#ff4444';
        body.innerHTML=_kpiHtml(el,d.avg_ms,c,type);
    }
    else if(type==='kpi_month_count'){
        const d=await(await fetch('/api/widget-data/month_count')).json();
        body.innerHTML=_kpiHtml(el,Number(d.count).toLocaleString(),'#45b7d1',type);
    }
    // ===== 장비 이상 현황 =====
    else if(type==='kpi_equipment_alert'){
        const d=await(await fetch('/api/widget-data/equipment_alert')).json();
        const bw=el.offsetWidth,bh=el.offsetHeight;
        const numFs=Math.max(18,Math.min(56,Math.min(bw/4.5,bh/2)));
        const lblFs=Math.max(11,numFs*0.35);
        const blink=v=>v>0?' class="eq-blink"':'';
        let h='<div style="display:flex;gap:8px;padding:8px;height:100%;align-items:center;justify-content:center">';
        h+='<div style="flex:1;text-align:center;cursor:pointer" onclick="location.href=\'/monitoring\'"><div data-eq-num'+blink(d.offline)+' style="font-size:'+numFs+'px;font-weight:bold;color:#ff6b6b">'+d.offline+'</div><div data-eq-lbl style="font-size:'+lblFs+'px;color:#aaa">오프라인</div></div>';
        h+='<div style="flex:1;text-align:center;cursor:pointer" onclick="location.href=\'/monitoring\'"><div data-eq-num'+blink(d.device_errors)+' style="font-size:'+numFs+'px;font-weight:bold;color:#ff4444">'+d.device_errors+'</div><div data-eq-lbl style="font-size:'+lblFs+'px;color:#aaa">장치오류</div></div>';
        h+='<div style="flex:1;text-align:center;cursor:pointer" onclick="location.href=\'/monitoring\'"><div data-eq-num'+blink(d.printer_warnings)+' style="font-size:'+numFs+'px;font-weight:bold;color:#feca57">'+d.printer_warnings+'</div><div data-eq-lbl style="font-size:'+lblFs+'px;color:#aaa">프린터경고</div></div>';
        h+='</div>';body.innerHTML=h;
    }
    // ===== 테이블: ISV 목록 =====
    else if(type==='isv_list'){
        const d=await(await fetch('/api/widget-data/isv_list')).json();
        let h='<table><tr><th>ISV</th><th style="text-align:right">키오스크</th></tr>';
        (d.isv||d.items||[]).forEach(i=>{h+='<tr><td>'+i.name+'</td><td style="text-align:right;color:#4ecdc4">'+(i.count||i.kiosk_count)+'</td></tr>';});
        body.innerHTML=h+'</table>';
    }
    // ===== 테이블: 최근 사용 =====
    else if(type==='recent_usage'){
        const d=await(await fetch('/api/widget-data/recent_usage')).json();
        let h='<table><tr><th>병원</th><th>키오스크</th><th>날짜</th><th style="text-align:right">건수</th></tr>';
        (d.data||d.items||[]).forEach(i=>{h+='<tr><td>'+i.name+'</td><td>'+(i.kiosk||i.kiosk_id)+'</td><td>'+i.date+'</td><td style="text-align:right;color:#4ecdc4">'+(i.count||i.total)+'</td></tr>';});
        body.innerHTML=h+'</table>';
    }
    // ===== 테이블: 알람 목록 =====
    else if(type==='alarm_list'){
        const d=await(await fetch('/api/widget-data/alarm_list')).json();
        let h='<table><tr><th>시간</th><th>병원</th><th>유형</th><th>심각도</th><th>상태</th></tr>';
        (d.data||d.items||[]).forEach(i=>{
            let sc=i.severity==='critical'?'#ff4757':'#feca57';
            h+='<tr><td>'+(i.time||'').substring(5,16)+'</td><td>'+(i.hosp||i.hosp_cd)+'</td><td>'+i.type+'</td><td style="color:'+sc+'">'+i.severity+'</td><td>'+i.status+'</td></tr>';
        });
        body.innerHTML=h+'</table>';
    }
    // ===== 테이블: 티켓 목록 =====
    else if(type==='ticket_list'){
        const d=await(await fetch('/api/widget-data/ticket_list')).json();
        let h='<table><tr><th>제목</th><th>우선순위</th><th>상태</th><th>생성일</th></tr>';
        (d.data||d.items||[]).forEach(i=>{
            let pc=i.priority==='high'?'#ff4757':i.priority==='medium'?'#feca57':'#999';
            h+='<tr><td>'+i.title+'</td><td style="color:'+pc+'">'+i.priority+'</td><td>'+i.status+'</td><td>'+(i.time||'').substring(5,16)+'</td></tr>';
        });
        body.innerHTML=h+'</table>';
    }
    // ===== 테이블: 에이전트 상태 =====
    else if(type==='agent_status'){
        const d=await(await fetch('/api/widget-data/agent_status')).json();
        let h='<table><tr><th>병원</th><th>키오스크</th><th>상태</th><th>CPU</th><th>MEM</th></tr>';
        (d.data||d.items||[]).forEach(i=>{
            let sc=i.status==='online'?'#2ed573':i.status==='error'?'#ff4757':'#999';
            h+='<tr><td>'+(i.hosp||i.hosp_cd)+'</td><td>'+(i.kiosk||i.kiosk_id)+'</td><td style="color:'+sc+'">'+i.status+'</td><td>'+i.cpu+'%</td><td>'+(i.mem||i.memory)+'%</td></tr>';
        });
        body.innerHTML=h+'</table>';
    }
    // ===== 테이블: 장애 키오스크 =====
    else if(type==='table_error_kiosks'){
        const d=await(await fetch('/api/widget-data/error_kiosks')).json();
        if((!d.data||d.data.length===0)){body.innerHTML='<div style="text-align:center;padding:20px;color:#666">장애 키오스크 없음</div>';return;}
        let h='<table><tr><th>병원</th><th>키오스크</th><th>CPU</th><th>MEM</th><th>프린터</th><th>EMR</th></tr>';
        (d.data||d.items||[]).forEach(i=>{h+='<tr><td>'+(i.hosp||i.hosp_cd)+'</td><td>'+(i.kiosk||i.kiosk_id)+'</td><td>'+i.cpu+'%</td><td>'+(i.mem||i.memory)+'%</td><td style="color:'+(i.printer==='error'||i.printer_a4==='error'?'#ff4757':'#2ed573')+'">'+(i.printer||i.printer_a4)+'</td><td style="color:'+(i.emr==='error'||i.emr_connection==='error'?'#ff4757':'#2ed573')+'">'+(i.emr||i.emr_connection)+'</td></tr>';});
        body.innerHTML=h+'</table>';
    }
    // ===== 테이블: 미응답 키오스크 =====
    else if(type==='table_no_heartbeat'){
        const d=await(await fetch('/api/widget-data/no_heartbeat')).json();
        const items=d.data||[];const show=items.slice(0,10);
        let h='<div style="overflow-y:auto;height:100%"><table style="width:100%;border-collapse:collapse;text-align:left"><tr><th style="text-align:left">병원</th><th style="text-align:left">키오스크</th><th style="text-align:left">미응답</th></tr>';
        if(show.length===0){h+='<tr><td colspan="3" style="text-align:center;color:#00ff88">모두 응답중</td></tr>';}
        else{show.forEach(r=>{const tc=r.time&&r.time.includes('일')?'#ff6b6b':'#feca57';h+='<tr><td>'+r.hosp+'</td><td>'+r.kiosk+'</td><td style="color:'+tc+';white-space:nowrap">'+r.time+'</td></tr>';});}
        h+='</table>';
        if(items.length>10)h+='<div style="text-align:center;padding:4px;color:#889;font-size:0.75em">총 '+items.length+'건</div>';
        h+='</div>';body.innerHTML=h;
    }
    // ===== 테이블: 오늘 TOP10 =====
    else if(type==='table_top10_today'){
        const d=await(await fetch('/api/widget-data/top10_today')).json();
        if((!d.data||d.data.length===0)){body.innerHTML='<div style="text-align:center;padding:20px;color:#666">오늘 이용 데이터 없음</div>';return;}
        let h='<table><tr><th>#</th><th>병원</th><th style="text-align:right">건수</th></tr>';
        (d.data||d.items||[]).forEach((i,idx)=>{h+='<tr><td>'+(idx+1)+'</td><td>'+i.name+'</td><td style="text-align:right;color:#4ecdc4;font-weight:bold">'+Number(i.count).toLocaleString()+'</td></tr>';});
        body.innerHTML=h+'</table>';
    }
    // ===== 테이블: 스냅샷 TOP =====
    else if(type==='table_snapshot_top'){
        const d=await(await fetch('/api/widget-data/snapshot_detail')).json();
        if(!d.items||d.items.length===0){body.innerHTML='<div style="text-align:center;padding:20px;color:#666">스냅샷 데이터 없음</div>';return;}
        let h='<table><tr><th>#</th><th>병원</th><th>키오스크</th><th style="text-align:right">건수</th></tr>';
        (d.items||[]).forEach((i,idx)=>{h+='<tr><td>'+(idx+1)+'</td><td>'+i.name+'</td><td>'+i.kiosks+'대</td><td style="text-align:right;color:#4ecdc4;font-weight:bold">'+Number(i.count).toLocaleString()+'</td></tr>';});
        body.innerHTML=h+'</table>';
    }
    // ===== 차트: 주간 추이 =====
    else if(type==='weekly_chart'){
        const d=await(await fetch('/api/widget-data/weekly_trend')).json();
        const items=d.data||[];
        _makeChart(body, id, {type:'line',data:{labels:items.map(x=>x.date.slice(5)),datasets:[{label:'이용건수',data:items.map(x=>x.count),borderColor:'#4ecdc4',backgroundColor:'rgba(78,205,196,0.15)',fill:true,tension:0.3}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:_chartScales()}});
    }
    // ===== 차트: ISV 도넛 =====
    else if(type==='isv_chart'){
        const d=await(await fetch('/api/widget-data/isv_list')).json();
        const items=d.isv||d.items||[];
        _makeChart(body, id, {type:'bar',data:{labels:items.map(x=>x.name),datasets:[{label:'키오스크',data:items.map(x=>x.count||x.kiosk_count),backgroundColor:CHART_COLORS.slice(0,items.length)}]},options:{responsive:true,maintainAspectRatio:false,indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{ticks:{color:'#fff',font:{size:12}},grid:{display:false}},y:{ticks:{color:'#fff',font:{size:14,weight:'bold'}},grid:{display:false}}}}});
    }
    // ===== 차트: 월별 추이 =====
    else if(type==='chart_monthly'){
        const d=await(await fetch('/api/widget-data/monthly_trend')).json();
        const items=d.data||[];
        _makeChart(body, id, {type:'bar',data:{labels:items.map(x=>x.month),datasets:[{label:'건수',data:items.map(x=>x.count),backgroundColor:'#a855f744',borderColor:'#a855f7',borderWidth:1}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:_chartScales()}});
    }
    // ===== 차트: 시간대별 =====
    else if(type==='chart_hourly'){
        const d=await(await fetch('/api/widget-data/hourly_usage')).json();
        _makeChart(body, id, {type:'line',data:{labels:d.labels||[],datasets:[{label:'건수',data:d.data||d.counts||[],borderColor:'#00ff88',backgroundColor:'#00ff8822',fill:true,tension:0.3}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:_chartScales()}});
    }
    // ===== 차트: ISV 오늘 =====
    else if(type==='chart_isv_today'){
        const d=await(await fetch('/api/widget-data/isv_today')).json();
        const items=d.data||[];
        _makeChart(body, id, {type:'bar',data:{labels:items.map(x=>x.isv),datasets:[{label:'건수',data:items.map(x=>x.count),backgroundColor:CHART_COLORS.slice(0,items.length)}]},options:{responsive:true,maintainAspectRatio:false,indexAxis:'y',plugins:{legend:{display:false}},scales:_chartScales()}});
    }
    // ===== 차트: 일별 이용 추이 =====
    else if(type==='chart_daily_trend'){
        const d=await(await fetch('/api/widget-data/daily_trend')).json();
        _makeChart(body, id, {type:'bar',data:{labels:d.labels,datasets:[{label:'이용건수',data:d.counts,backgroundColor:'rgba(0,212,255,0.4)',borderColor:'#00d4ff',borderWidth:1},{label:'가동병원',data:d.hospitals,type:'line',borderColor:'#00ff88',yAxisID:'y1',tension:0.3}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:'#fff',font:{size:12}}}},scales:Object.assign(_chartScales(),{y1:{position:'right',ticks:{color:'#00ff88',font:{size:12}},grid:{display:false}}})}});
    }
    // ===== 차트: 일별 병원 추이 =====
    else if(type==='chart_daily_hosp'){
        const d=await(await fetch('/api/widget-data/daily_hospital_trend')).json();
        _makeChart(body, id, {type:'line',data:{labels:d.labels,datasets:[{label:'전체병원',data:d.total,borderColor:'#4ecdc4',tension:0.3},{label:'가동병원',data:d.active,borderColor:'#00ff88',tension:0.3}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:'#fff',font:{size:12}}}},scales:_chartScales()}});
    }
    // ===== 시계 =====
    else if(type==='clock'){
        const bw=el.offsetWidth,bh=el.offsetHeight;
        const tfs=Math.max(14,Math.min(42,Math.min(bw/5,bh/2.5)));
        const dfs=Math.max(10,tfs*0.4);
        const update=()=>{
            const now=new Date();
            const days=['일','월','화','수','목','금','토'];
            const hh=String(now.getHours()).padStart(2,'0'),mm=String(now.getMinutes()).padStart(2,'0'),ss=String(now.getSeconds()).padStart(2,'0');
            const y=now.getFullYear(),mo=String(now.getMonth()+1).padStart(2,'0'),dd=String(now.getDate()).padStart(2,'0');
            body.innerHTML='<div style="text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%"><div data-clock-time style="font-size:'+tfs+'px;font-weight:bold;color:#4ecdc4">'+hh+':'+mm+':'+ss+'</div><div data-clock-date style="color:#aaa;font-size:'+dfs+'px;margin-top:4px">'+y+'.'+mo+'.'+dd+' ('+days[now.getDay()]+')</div></div>';
        };
        update();setInterval(update,1000);
    }
    // ===== 텍스트 =====
    else if(type==='text_block'){
        if(!body.textContent||body.textContent==='로딩중...') body.innerHTML='<div style="padding:8px;color:#ccc">텍스트 블록</div>';
    }
    // ===== 알수없는 위젯 =====
    else {
        body.innerHTML='<div style="color:#666;text-align:center;margin-top:10px">'+type+'</div>';
    }
    } catch(e) {
        body.innerHTML='<span style="color:#f66;font-size:0.7rem">로드실패</span>';
    }
}

function applyWidgetScale(el) {
    const w=el.offsetWidth, h=el.offsetHeight;
    const type=el.dataset?el.dataset.type:(el.getAttribute('data-type')||'');
    const def=(typeof WIDGET_DEFS!=='undefined'&&WIDGET_DEFS[type])?WIDGET_DEFS[type]:null;
    const bw=def?def.w:160, bh=def?def.h:100;
    const scale=Math.max(0.6,Math.min(3,Math.min(w/bw,h/bh)));
    const body=el.querySelector('.w-body');
    if(!body) return;

    // KPI 값
    const kv=body.querySelector('.kpi-val');
    if(kv){
        const numFs=Math.max(16,Math.min(80,Math.min(w/3.5,h/2)));
        kv.style.fontSize=numFs+'px';
    }

    // 장비이상현황 - 숫자와 라벨 크기 조정
    const eqNums=body.querySelectorAll('[data-eq-num]');
    if(eqNums.length>0){
        const numFs=Math.max(16,Math.min(48,Math.min(w/5,h/2.5)));
        eqNums.forEach(n=>{n.style.fontSize=numFs+'px';});
        body.querySelectorAll('[data-eq-lbl]').forEach(l=>{l.style.fontSize=Math.max(10,numFs*0.4)+'px';});
    }

    // 시계 크기 조정
    const clockTime=body.querySelector('[data-clock-time]');
    if(clockTime){
        const tfs=Math.max(14,Math.min(42,Math.min(w/5,h/2.5)));
        clockTime.style.fontSize=tfs+'px';
        const clockDate=body.querySelector('[data-clock-date]');
        if(clockDate) clockDate.style.fontSize=Math.max(10,tfs*0.4)+'px';
    }

    // 테이블 크기 조정
    const tbl=body.querySelector('table');
    if(tbl){
        const ts=Math.min(w/(bw||200),h/(bh||200));
        tbl.querySelectorAll('th').forEach(t=>{t.style.fontSize=Math.max(0.4,0.6*ts)+'rem';t.style.padding=Math.max(0,1*ts)+'px '+Math.max(1,2*ts)+'px';});
        tbl.querySelectorAll('td').forEach(t=>{t.style.fontSize=Math.max(0.45,0.65*ts)+'rem';t.style.padding=Math.max(0,1*ts)+'px '+Math.max(1,2*ts)+'px';});
    }

    // 헤더
    const hdr=el.querySelector('.w-header');
    if(hdr){
        hdr.style.fontSize=Math.max(0.85,1.1*scale)+'rem';
        hdr.style.padding='8px 14px';
    }
}
