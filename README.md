# sentinelGPT

Speed up the analysis of suspicious activities coming from SentinelOne. Using chatGPT API with different models: 3.5, 4 and 4-preview.

The script follows an ETL structure: Extract - Transform and Load.

- **Extract** -> events are extracted from SentinelOne based on a query (generally advisable to use a Storyline ID)
- **Transform** -> data extracted from SentinelOne is anonymized. Key names. Data related to endpoints, names or user paths.
- **Load** -> the data is sent via API to chatGPT for analysis.

The calling instruction to GPT follows the investigation [LARGE LANGUAGE MODELS AS OPTIMIZERS](https://arxiv.org/pdf/2309.03409.pdf)

Quote from the document:
- The styles of instructions found by different optimizer LLMs vary a lot: PaLM 2-L-IT and text-bison ones are concise, while GPT ones are long and detailed.
- Although some top instructions contain the “step-by-step” phrase, most others achieve a comparable or better accuracy with different semantic meanings
- **GPT3.5** optimize prompt: **A little bit of arithmetic and a logical approach will help us quickly arrive at the solution to this problem**
- **GPT4** optimize prompt: **Let’s combine our numerical command and clear thinking to quickly and accurately decipher the answer**.

**Examples**
------------------------
1. **Easy behaviour to analyse:** Suspicious command enumeration from windows terminal:

cmd /k "whoami /priv && ping 127.0.0.1 && netstat -nato && tasklist && systeminfo"
![image](https://github.com/RazviAlex/sentinelGPT/assets/51793648/457a42be-e0b7-4b0b-bd1c-3999739ddb61)

2. **Hard behaviour to analyse:** Using [msbuild lolbin](https://www.ired.team/offensive-security/code-execution/using-msbuild-to-execute-shellcode-in-c) to perfom a priviliege escalation:

"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\msbuild.exe" C:\temp\readme.txt
![image](https://github.com/RazviAlex/sentinelGPT/assets/51793648/ba8bbd2f-589e-4956-b4b8-b6ebcccad296)

In that case, is obersevered that the GPT 3.5 model is not enough to proper analyse the behaviour of the msbuild execution. So model 4 is used, giving a better understading of what happens:
![image](https://github.com/RazviAlex/sentinelGPT/assets/51793648/1470aaae-c5c3-4dbb-8be3-e1af28467951)
