from twitterpibot.schedule.ScheduledTask import ScheduledTask

agile_manifesto = [
    "We are uncovering better ways of developing software by doing it and helping others do it. Through this work we have come to value:",

    "Individuals and interactions over processes and tools",
    "Working software over comprehensive documentation",
    "Customer collaboration over contract negotiation",
    "Responding to change over following a plan",

    "That is, while there is value in the items on the right, we value the items on the left more."
]

agile_principles = [
    "Principles behind the Agile Manifesto:",
    "Our highest priority is to satisfy the customer through early and continuous delivery of valuable software.",
    "Welcome changing requirements, even late in development. Agile processes harness change for the customer's competitive advantage."
    "Deliver working software frequently, from a couple of weeks to a couple of months, with a preference to the shorter timescale.",
    "Business people and developers must work together daily throughout the project.",
    "Build projects around motivated individuals. Give them the environment and support they need, and trust them to get the job done.",
    "The most efficient and effective method of conveying information to and within a development team is face-to-face conversation.",
    "Working software is the primary measure of progress.",
    "Agile processes promote sustainable development. The sponsors, developers, and users should be able to maintain a constant pace indefinitely.",
    "Continuous attention to technical excellence and good design enhances agility.",
    "Simplicity, the art of maximizing the amount of work not done, is essential.",
    "The best architectures, requirements, and designs emerge from self-organizing teams.",
    "At regular intervals, the team reflects on how to become more effective, then tunes and adjusts its behavior accordingly.",
]

toyota = [
    "Plan -> Do -> Check -> Act",
    "Continuous Improvement",
    "Respect for People",
    "CHALLENGE: To maintain a long-term vision and meet all challenges with the courage and creativity needed to realise that vision.",
    "KAIZEN: Continuous improvement. As no process can ever be declared perfect, there is always room for improvement.",
    "GENCHI GENBUTSU: Going to the source to find the facts to make correct decisions, build consensus and achieve goals.",
    "RESPECT: Respect others, makes every effort to understand others, accepts responsibility and does its best to build mutual trust.",
    "TEAMWORK: stimulates personal and professional growth, shares opportunities for development and maximises individual and team performance.",

    "Just-in-Time – smooth, continuous, optimised workflows",
    "HEIJUNKA – LEVELLING THE FLOW",
    "ELIMINATION OF WASTE – MUDA",
    "TAKT TIME – THE HEARTBEAT OF PRODUCTION",
    "KANBAN",

    "Jidoka – building in quality",
    "GENCHI GENBUTSU – GOING TO THE SOURCE ",
    "ANDON BOARD",
    "STANDARDISATION",
    "MISTAKE-PROOFING AND LABELLING",

    "Kaizen – improvement is a continuous process",
    "TPS – THE ‘THINKING PEOPLE SYSTEM’",
    "TESTING THE LOGIC – ‘5 WHYS?’",
    "A CULTURE OF CONTINUOUS IMPROVEMENT – ‘5S’",
    "SEIRI – Sifting",
    "SEITON – Sorting",
    "SEISO – Sweeping and cleaning",
    "SEIKETSU – Spic-and-span",
    "SHITSUKE – Sustain",

    # glossary

    "Andon Board – The facility for workers to signal problems to supervisors for immediate remedy, stopping the production process if necessary. Workstations along the production line can activate a warning on an illuminated central display board, which constantly displays productivity levels.",
    "Asa-ichi Meeting – A meeting held every morning in Toyota plants to discuss quality deviations and eliminate their causes. An essential part of the practice of kaizen.",
    "Genchi Genbutsu – Going to the source to find the facts to make correct decisions, build consensus and achieve goals.",
    "Heijunka – Levelling the production schedule in both volume and variety. A precondition for just-in-time and elimination of mura, muri and muda.",
    "Jidoka – Making problems visible so that they can be immediately addressed.",
    "Just-in-Time – Making only what is needed, when it is needed, and in the amount needed, delivered just as they are needed (a continuous ‘pulling’ flow of standardised operations).",
    "Kaizen – Continuous improvement. As no process can ever be declared perfect, there is always room for improvement.",
    "Kanban Card – An instruction in the process that parts need to be replenished for production to continue uninterrupted.",
    "Muda – Waste in all its forms (things that do not add value to the final product): overproduction, surplus inventory, rework/correction, motion, processing, waiting and conveyance.",
    "Mura – Unevenness (in workload). Heijunka eliminates mura, muri and muda.",
    "Muri – Overburden or strenuous work, leading to safety and quality problems – more waste.",
    "Poka-Yoke – Mistake-proofing – devices that make it difficult or impossible for a worker to make common errors at his or her workstation. A simple but creative and reliable way to reduce errors and maintain quality.",
    "Pull-System – Items called only as they are needed, as opposed to a ‘push-system’ that may not take account of actual need.",
    "Takt Time – The rate of customer demand – producing only what the market requires, and thereby achieving the optimum duration of the work-cycle that fulfils each customer’s demand.",

]
misc = ["Any sufficiently advanced technology  is indistinguishable from magic - Arthur C Clarke"]


class DeveloperWisdomScheduledTask(ScheduledTask):
    pass
