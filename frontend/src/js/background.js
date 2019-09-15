/* eslint-disable no-undef */
import '../img/icon-128.png';
import '../img/icon-34.png';
import { ARTICLES } from './endpoints';
import fetcher from './fetcher';

// chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
//   if (changeInfo.status == 'complete' && tab.active) {
//     try {
//       const { data } = await fetcher.post(ARTICLES, {
//         title: 'Test 123',
//         domain: 'wyborcza.pl',
//         publication_date: '20.07.2018'
//       });
//       console.log(data);
//       if (data) {
//         chrome.extension.sendMessage(data, res => console.log(res));
//       }
//     } catch (error) {
//       throw new Error(error);
//     }
//   }
// });

chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  // chrome.tabs.query({ active: true, currentWindow: true }, async tabs => {
  if (changeInfo.status === 'complete' && tab.active) {
    try {
      const { data } = await fetcher.post(ARTICLES, {
        title: 'Test 123',
        domain: 'wyborcza.pl',
        publication_date: '20.07.2018'
      });

      chrome.tabs.sendMessage(tabId, { type: 'articlesData', ...data }, async response => {
        // chrome.tabs.sendMessage(tabs[0].id, { type: 'articlesData', ...data }, async response => {
        if (response.type === 'articlesReceived') {
          await console.log('Articles received');
        }
      });
    } catch (error) {
      throw new Error(error);
    }
  }
});
