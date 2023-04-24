fetch('/news')
.then(response => response.json())
.then(data => {
  const articles = data.articles;
  const newsDiv = document.getElementById('news');
  for (let article of articles) {
    const articleDiv = document.createElement('div');
    articleDiv.innerHTML = `
      <h2>${article.title}</h2>
      <p>${article.description}</p>
      <img src="${article.urlToImage}" alt="${article.title}">
      <a href="${article.url}">Read more</a>
    `;
    newsDiv.appendChild(articleDiv);
  }
});