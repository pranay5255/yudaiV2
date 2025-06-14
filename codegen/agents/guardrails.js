class GuardrailTripwireTriggered extends Error {}

const BLOCKLIST = [
  'DROP TABLE',
  'DELETE FROM',
  'TRUNCATE',
  '--',
  ';',
];

function checkSafety(text) {
  const upper = text.toUpperCase();
  for (const word of BLOCKLIST) {
    if (upper.includes(word)) {
      throw new GuardrailTripwireTriggered('Unsafe content detected');
    }
  }
  return true;
}

module.exports = { GuardrailTripwireTriggered, checkSafety };
