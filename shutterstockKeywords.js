// ==UserScript==
// @name          Shutterstock Keywords New design v2
// @author        idea: Oleg Skillup http://skillup.lj.ru improvement: Chat in telegram/discord @MicrostockPatreon
// @source        Open Source
// @version       2.220627
// @description   Easy to copy image keywords.
// @match       https://www.shutterstock.com/*
// @match       https://www.m-rank.net/*
// @grant         GM_xmlhttpRequest
// ==/UserScript==

(() => {
    let newKeywords = document.createElement("div"),
        lastModifiedDiv = document.createElement("div");
newKeywords.style.cssText = `
position: relative;
background-color: white;
padding: 10px;`;

    let divArray = document.querySelectorAll('.MuiContainer-root');
    let divSelect = [].filter.call(divArray, function(el) {
        if (el.classList.length == 4){
            return el;
        }
    });
    console.log(divSelect[0]); //.jss233
    divSelect[0].appendChild(newKeywords);
    //divArray[2].appendChild(newKeywords);
    //document.querySelector(`.jss233`).appendChild(newKeywords);

    const getKeywords = () => JSON.parse(document.getElementById("__NEXT_DATA__").innerText).props.pageProps.asset.keywords
    const getKeywordsEl = () => getKeywords().length > 0

    const getMrankEl = () => document.getElementById('mrankPosition')

    let updateWords = () => {
        let keywords = getKeywords()
        const words = getKeywords()
        let sortedIndex = 0;
        for (let i = words.length - 1; i > 0; i--)
        {
            if (words[i] < words[i-1]) {
                sortedIndex = i;
                break;
            }
        }
        console.log("found sortedIndex", sortedIndex, words[sortedIndex], words[sortedIndex-1])

        let soldWords = '';
        let notSoldWords = '';
        for (let i = 0; i < words.length -1; i++) {
            if (sortedIndex && i < sortedIndex) {
                soldWords += `<a style="color: #26bd7e;" href="/search/${words[i]}">${words[i]}</a>, `;
            } else {
                notSoldWords += `<a style="color: #0070f0;" href="/search/${words[i]}">${words[i]}</a>, `;
            }
        }

        if (soldWords.length > 0) {
            soldWords = soldWords.substring(0, soldWords.length-2);
        }

        if (notSoldWords.length > 0) {
            notSoldWords = notSoldWords.substring(0, notSoldWords.length-2);
        }

        let resultList = '';
        if (soldWords.length > 0) {
            resultList += `<br><span style="color: #26bd7e; font-weight: bold;">Sold(${sortedIndex}):</span><br>`
            resultList += `<span>${soldWords}</span><br>`;
        }

        let notSold = words.length - sortedIndex;
        if (notSoldWords.length > 0) {
            resultList += `<br><span style="color: #0070f0; font-weight: bold;">Not sold(${notSold}):</span><br>`;
        }

        if (notSoldWords.length > 0) {
            resultList += `<span>${notSoldWords}</span>`;
        }

        resultList += `<br><br><span style="font-weight: bold;">Mrank: </span><span id="mrankPosition" style='color: #000;'></span>`;

        newKeywords.innerHTML = `<style>a {text-decoration: none;}a:hover {text-decoration: underline;}</style>
                <p><span>Keywords(${words.length})</span><br>${resultList}</p>`;
        newKeywords.style.display='block';

       const imageID = document.URL.split("-").pop(),
             mrankURL = `http://m-rank.net/?search=${imageID}`;
        console.log("mrankURL", mrankURL)

        GM_xmlhttpRequest({
        method: "GET",
        url: mrankURL,
        onload: function(response) {
            const mrankEl = getMrankEl()
            if(!mrankEl) return;
            if (response.status != 200) {
                mrankEl.innerHTML = response.status + ': ' + response.statusText;
            } else {
                let temp = response.responseText.match(/tle>\d+/) || 'вне топа';
                let date = response.responseText.match(/\d\d\d\d\.\d\d\.\d\d/)

                let position = temp === 'вне топа' ? temp : `позиция ${temp[0].replace(/(tle>)(\d+)/g, '$2')}`;
                position += date && date[0] ? `, загружено ${date[0]}` : ''
                mrankEl.innerHTML = position
            }
        }
    });
    }
    let shouldUpdate = false
    const debounceUpdateWords = () => {
        if(shouldUpdate) return
        shouldUpdate = true
        setTimeout(() => {
            if(shouldUpdate) {
                updateWords()
                shouldUpdate = false
            }
        }, 1000)
    }

    const clear = () => {
        if(!getKeywordsEl()) {
            newKeywords.innerHTML = '';
            newKeywords.style.display='none';
            const mrankEl = document.getElementById('mrankPosition')
            if(getMrankEl()) {
                getMrankEl().innerHTML = '';
            }
            return
        }
    }

    const once = (fn, context) => {
        var result;
        return function() {
            if (fn) {
                result = fn.apply(context || this, arguments);
                fn = null;
            }
            return result;
        };
    }
    let querySelector = getKeywordsEl()
    querySelector ? updateWords() : clear()
    document.querySelector('body').addEventListener('DOMSubtreeModified', () => {
        clear()
        once(debounceUpdateWords)
    })
})();
