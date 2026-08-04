# Reflection

I used an AI coding assistant to help plan, implement, test, review, and document two features for this Task Tracker: due dates with overdue filtering, and tags with tag filtering. I used AI most effectively when the request was constrained. For example, asking for an optional ISO date, a precise overdue rule, a PATCH update, and focused pytest coverage produced a useful starting point. Broad prompts such as “add due dates” were much less helpful because they left important behavior undefined.

One moment where AI helped was identifying edge cases that were easy to overlook. It suggested testing invalid date input, overdue filtering, and update behavior. This helped turn a visual feature into a properly verified backend change. It also helped structure the Pydantic validators for trimmed, non-empty tags.

AI slowed me down when it proposed designs that were too ambitious for the assignment. One suggestion was to introduce normalized tag tables and persistence. That design could be appropriate in a larger application, but it would have added migrations, repositories, and database setup that were not necessary for this scoped project. I rejected that option and kept tags as a validated list on each in-memory task.

My review changed the result in several places. The most important correction was the overdue rule. A simple “due date before today” calculation incorrectly marks completed tasks as overdue. I changed the rule so tasks with status `done` are excluded. I also added HTML escaping before rendering user-entered values, which was not included in the first frontend draft.

The project reinforced that AI output should be treated as a proposal rather than an answer. Small prompts, explicit constraints, focused tests, manual browser checks, and Break Tests made the final result easier to understand and defend.
