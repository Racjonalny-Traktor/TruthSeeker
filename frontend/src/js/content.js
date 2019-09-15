import '../css/content.css';

import snackbar, { setFlag } from './content/snackbar';

/* eslint-disable no-undef */
chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
  if (request.type === 'articlesData') {
    sendResponse({ type: 'articlesReceived' });
    const {
      is_objective: isObjective,
      it_too_old: isTooOld,
      opposition_articles: oppositionArticles
    } = request;
    setFlag(isObjective);
  }
});

// Inject element
const body = document.querySelector('body');
body.appendChild(snackbar);
