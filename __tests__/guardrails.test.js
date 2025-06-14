const { checkSafety, GuardrailTripwireTriggered } = require('../codegen/agents/guardrails.js');

test('escalates on DROP TABLE', () => {
  expect(() => checkSafety('DROP TABLE users;')).toThrow(GuardrailTripwireTriggered);
});
