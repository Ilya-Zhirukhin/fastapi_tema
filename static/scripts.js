document.getElementById('theme-toggle').addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.innerHTML = document.body.classList.contains('dark-theme')
        ? '<i class="fas fa-lightbulb"></i>'
        : '<i class="far fa-lightbulb"></i>';
});


// document.getElementById('get-balance-btn').addEventListener('click', getBalance);
// document.getElementById('get-token-info-btn').addEventListener('click', getTokenInfo);
// document.getElementById('get-top-addresses-btn').addEventListener('click', getTopAddresses);

// async function getBalance() {
//     const address = document.getElementById('address').value;
//     const loader = document.getElementById('balance-loader');
//     loader.style.display = 'inline-block';

//     try {
//         const response = await fetch(`/get_balance?address=${address}`);
//         const data = await response.json();
//         document.getElementById('balance-result').innerHTML = `
//             <div class="result">
//                 <p>Balance: ${data.balance}</p>
//             </div>
//         `;
//     } catch (error) {
//         console.error('Error:', error);
//     }

//     loader.style.display = 'none';
// }

// async function getTokenInfo() {
//     const loader = document.getElementById('token-info-loader');
//     loader.style.display = 'inline-block';

//     try {
//         const response = await fetch('/get_token_info');
//         if (!response.ok) {
//             throw new Error('Failed to fetch token info');
//         }
//         const data = await response.json();
//         document.getElementById('token-info-result').innerHTML = `
//             <div class="result">
//                 <p>Name: ${data.name}</p>
//                 <p>Symbol: ${data.symbol}</p>
//                 <p>Total Supply: ${data.totalSupply}</p>
//             </div>
//         `;
//     } catch (error) {
//         console.error('Error:', error);
//         document.getElementById('token-info-result').innerHTML = `
//             <div class="error">
//                 <p>Failed to fetch token info. Please try again later.</p>
//             </div>
//         `;
//     }

//     loader.style.display = 'none';
// }


// async function getTopAddresses() {
//     const n = document.getElementById('top-n').value;
//     const loader = document.getElementById('top-addresses-loader');
//     loader.style.display = 'inline-block';

//     try {
//         const response = await fetch(`/get_top?n=${n}`);
//         if (!response.ok) {
//             throw new Error('Failed to fetch top addresses');
//         }
//         const data = await response.json();
//         const topAddresses = data.top_addresses.map(([address, balance]) => `
//             <p>${address}: ${balance}</p>
//         `).join('');
//         document.getElementById('top-addresses-result').innerHTML = `
//             <div class="result">
//                 <h3>Top Addresses:</h3>
//                 ${topAddresses}
//             </div>
//         `;
//     } catch (error) {
//         console.error('Error:', error);
//         document.getElementById('top-addresses-result').innerHTML = `
//             <div class="error">
//                 <p>Failed to fetch top addresses. Please try again later.</p>
//             </div>
//         `;
//     }

//     loader.style.display = 'none';
// }
