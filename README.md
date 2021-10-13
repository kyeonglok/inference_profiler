# inference_profiler
inference profiler는 triton inference server를 사용하여 추론 작업에서 구간별 추론 스택과 OS 커널의 전계층을 프로파일링 할 수 있는 프로파일러입니다.
커널 스택 분석을 위한 ebpf 및 bpftrace를 활용한 프로파일링 기법과 NVIDIA triton inference server의 프로파일링 도구를 활용하여 통합 프로파일링 인터페이스를 제공합니다.

## eBPF및 bpftrace를 활용한 프로파일링

1. ebpf_trace.bt는 [bpftrace](https://github.com/iovisor/bpftrace)를 사용하여 작성된 프로그램입니다. 실행을 위해서는 먼저 [bpftrace를 설치](https://github.com/iovisor/bpftrace/blob/master/INSTALL.md)해야합니다.

 - Ubunutu OS에서는 다음의 명령어를 통해 bpftrace를 설치할 수 있습니다.
```
$ sudo apt-get install –y bpftrace 
```
2. 설치가 완료되었다면 다음의 명령어를 통해 프로그램을 실행할 수 있습니다.
```   
$ sudo ./ebpf_trace.bt 
 ``` 
3. 결과 예시
```
Attaching 3 probes. . .
Tracing tcp send/recv. Hit Ctrl-C to end.
TIME      PID    COMM              SADDR:SPORT              DADDR:DPORT           TIME(ms)       SEND/RECV
17:59:47  54643  image_client      127.0.0.1:33782          127.0.0.1:8000        2033           *SEND
17:59:47  54498  tritonserver      172.17.0.2:8000          172.17.0.1:58736      2033           *RECV
17:59:47  54498  tritonserver      172.17.0.2:8000          172.17.0.1:58736      2033           *SEND
. . .
```

## NVIDIA triton inference server의 프로파일링 도구를 활용한 프로파일링

1. [NVIDIA triton inference server](https://github.com/triton-inference-server/server)에서는 추론 과정에서의 구간 분석을 위한 [프로파일링 기능](https://github.com/triton-inference-server/server/blob/main/docs/trace.md)을 제공합니다. tritonserver 실행시 다음의 옵션을 추가하여 프로파일링 기능을 사용할 수 있습니다. --trace-file 옵션에서 지정해준 경로에 json 파일 형식으로 프로파일링 결과가 저장됩니다.  
```
$ tritonserver --trace-file=/tmp/trace.json --trace-rate=100 --trace-level=MAX ... 
``` 
2. tritonserver를 실행한 후 클라이언트에서 요청한 추론 작업을 완료하면 서버를 종료시킵니다. 그 후 다음의 명령어를 실행하면 json파일로 저장되어있는 정보를 분석하여 최종 프로파일링 결과가 출력됩니다.
```   
$ python3 triton_trace_parser.py  
```
3. 결과 예시
```
HTTP_RECV_START      HTTP_RECV_END        REQUEST_START        QUEUE_START          COMPUTE_START        COMPUTE_INPUT_END    COMPUTE_OUTPUT_START COMPUTE_END          REQUEST_END          HTTP_SEND_START      HTTP_SEND_END        
0 ns                 526015 ns            542254 ns            544639 ns            554494 ns            645533 ns            6312705 ns           6317666 ns           6334089 ns           6336647 ns           6340987 ns           
----+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+---------------->
           526015 ns             16239 ns              2384 ns              9855 ns             91038 ns           5667172 ns              4960 ns             16423 ns              2558 ns              4339 ns
```
