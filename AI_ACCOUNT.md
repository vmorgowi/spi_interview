# AI Account

1. **Which AI tools did you use?**

	Free Claude web interface with the Sonnet 5 Medium setting. 

2. **Why did you choose them?**

	My former coworkers spoke well of Claude. This specific version was free and met enough of my needs to get started.

3. **If cost and access were not constraints, would you have used different tools or
models? Why?**

	Having access to the paid version of Claude would have allowed me to use it directly with the code I was writing myself. As it was, I had to resort to copying over pieces from the code it generated and manually merging them with my own code. This process was slow and error-prone.

	That being said, going slowly and doing those manual merges gave me a greater understanding of how the code actually worked. While I would have tried the fully integrated version of Claude Code for the sake of comparison, I still might not have chosen to use it in the end.

	Overall, the extremely short time frame for this large of an assignment seemed intended to encourage heavy vibe-coding regardless of the tool or model used. I have instead tried to strike a balance between generating code while also writing some of it myself because of the potential need to explain and modify it in a follow-up interview.

4. **Where did the tools fail you, mislead you, or require meaningful correction?**

	* As typical with AI-generated code, the path of least resistance was to accept the application architecture it gave me. However, this made modifying and debugging the code more challenging, and encouraged further use of the AI to address issues that came up. I had to fight the AI to keep the code in a state I understood.
	* While the code Claude generated was workable for a throwaway prototype, the way it stylized the UI was fragile and relied on many hardcoded values. None of this would hold up for a tool that needed to gracefully handle resizing, let alone be polished into something production-ready.
	* The raw generated code frequently came with subtle issues with component sizing that I had to manually correct.
	* Claude's suggestions were theoretically helpful if time had not been a constraint, but I found most of them misleading in the context of this project. I had to choose very carefully what changes I wanted it to generate to not lose sight of my priorities.
	* In some cases, such as fixing a layout bug where part of the background did not display correctly, Claude's "solution" just created more code complexity while introducing other visual problems. For this issue, I had to debug it myself.