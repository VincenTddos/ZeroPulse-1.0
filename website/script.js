/* 購買和頁面導航邏輯 */

function scrollToPricing() {
    document.getElementById('pricing').scrollIntoView({ behavior: 'smooth' });
}

function purchase(planType) {
    // 簡單序號驗證系統
    const plans = {
        'month': 'NT$399/月',
        'quarter': 'NT$999/季',
        'lifetime': 'NT$2999/終身'
    };

    const serialPrefix = {
        'month': 'ZP-M',
        'quarter': 'ZP-Q',
        'lifetime': 'ZP-L'
    };

    // 生成測試序號
    const testSerial = serialPrefix[planType] + '-' + generateRandomSerial();

    alert(`
購買方案: ${plans[planType]}

測試序號: ${testSerial}

【購買流程】
1. 聯絡 Discord: ZeroPulse Community
2. 提供序號激活
3. 下載 ZeroPulse.exe
4. 進遊戲壓槍無敵！

此為演示版本。實際購買請聯絡客服。
    `);
}

function generateRandomSerial() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let serial = '';
    for (let i = 0; i < 12; i++) {
        serial += chars.charAt(Math.floor(Math.random() * chars.length));
        if ((i + 1) % 4 === 0 && i < 11) serial += '-';
    }
    return serial;
}

// 平滑滾動導航
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && document.querySelector(href)) {
            e.preventDefault();
            document.querySelector(href).scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});
