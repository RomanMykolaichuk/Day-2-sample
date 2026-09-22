const sleep = ms =>
  new Promise(resolve =>
    setTimeout(resolve, ms)
  );


async function addLog(text) {

  const log =
    document.getElementById("agentLog");

  log.textContent +=
    "\n\n" + text;

  log.scrollTop =
    log.scrollHeight;

  await sleep(650);
}


async function runAgent() {

  const mission =
    document
      .getElementById("mission")
      .value;


  const topic =
    document
      .getElementById("topic")
      .value
      .trim();


  const log =
    document.getElementById(
      "agentLog"
    );


  log.textContent =
    "AGENT STARTED";


  await addLog(
    "🎯 GOAL\n" +
    getGoal(
      mission,
      topic
    )
  );


  await addLog(
    "🧠 THINK\n" +
    "I need to break the objective into smaller tasks."
  );


  await addLog(
    "📋 PLAN\n" +
    getPlan(mission)
  );


  await addLog(
    "🛠️ ACTION 1\n" +
    "Collect relevant information."
  );


  await addLog(
    "👁️ OBSERVATION\n" +
    "Relevant information has been identified."
  );


  await addLog(
    "🛠️ ACTION 2\n" +
    "Organize and compare the information."
  );


  await addLog(
    "👁️ OBSERVATION\n" +
    "Main patterns and useful points identified."
  );


  await addLog(
    "🧠 REFLECTION\n" +
    "The result should now be checked against the original goal."
  );


  await addLog(
    "✅ FINAL RESULT\n" +
    getResult(
      mission,
      topic
    )
  );
}


function getGoal(
  mission,
  topic
) {

  const goals = {

    research:
      `Research: "${topic}" and identify the most useful findings.`,

    briefing:
      `Prepare a concise briefing about "${topic}".`,

    course:
      `Create a lesson plan about "${topic}".`,

    data:
      `Develop an analytical approach for "${topic}".`

  };


  return goals[mission];
}


function getPlan(mission) {

  const plans = {

    research:
`1. Define the research question
2. Collect information
3. Compare evidence
4. Identify key findings
5. Summarize`,

    briefing:
`1. Identify the audience
2. Extract important facts
3. Prioritize information
4. Draft briefing
5. Check clarity`,

    course:
`1. Define learning objectives
2. Select key concepts
3. Create explanation
4. Add practical activity
5. Create assessment`,

    data:
`1. Define the analytical question
2. Inspect the data
3. Select analytical methods
4. Interpret results
5. Present conclusions`

  };


  return plans[mission];
}


function getResult(
  mission,
  topic
) {

  const results = {

    research:
      `Research workflow for "${topic}" completed.`,

    briefing:
      `Briefing structure for "${topic}" prepared.`,

    course:
      `Lesson workflow for "${topic}" prepared.`,

    data:
      `Analytical workflow for "${topic}" prepared.`

  };


  return results[mission];
}


function clearLog() {

  document
    .getElementById(
      "agentLog"
    )
    .textContent =
`Agent ready.

Choose a mission and press "Run Agent".`;

}