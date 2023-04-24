fetch('/news')
.then(response => response.json())
.then(data => {
  const articles = data.articles;
  const newsDiv = document.getElementById('news');

  for (let article of articles) {
    const articleDiv = document.createElement('a');
    articleDiv.href = article.url;
    articleDiv.className = "flex mb-2 flex-col items-center  rounded-lg shadow md:flex-row md:max-w-xl  border-gray-700 bg-gray-800 hover:bg-gray-600"

    const articleImg = document.createElement('img');
    articleImg.src = article.urlToImage;
    articleImg.alt = article.title;
    articleImg.className = "object-cover w-full rounded-t-lg h-96 md:h-auto md:w-48 md:rounded-none md:rounded-l-lg "

    const articleText = document.createElement('div');
    articleText.className = "flex flex-col justify-between p-4 leading-normal"

    const articleTitle = document.createElement('h5');
    articleTitle.className = "mb-2 text-md font-bold tracking-tight text-white"
    const titleText = article.title.substr(0, 70);
    articleTitle.innerText = titleText + (article.title.length > 70 ? '...' : '');
    

    const articleDescription = document.createElement('p');
    articleDescription.className = "mb-3 text-xs font-normal text-gray-400"
    const descriptionText = article.description.substr(0, 100);
    articleDescription.innerText = descriptionText + (article.description.length > 100 ? '...' : '');
   

    articleText.appendChild(articleTitle);
    articleText.appendChild(articleDescription);

    articleDiv.appendChild(articleImg);
    articleDiv.appendChild(articleText);

    newsDiv.appendChild(articleDiv);
  }
});