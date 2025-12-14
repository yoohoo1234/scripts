// ==UserScript==
// @name         Magnet Link Helper: Copy & Open Localhost
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  点击磁力链接时复制链接并跳转到指定的本地服务页面
// @author       Perplexity
// @match        *://*/*
// @grant        GM_setClipboard
// @grant        GM_openInTab
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';

    // 目标跳转地址
    const TARGET_URL = "http://localhost:19798/?page=files&path=%2F%E8%BF%85%E9%9B%B7%E4%BA%91%E7%9B%98";

    // 使用事件委托监听所有点击事件
    document.addEventListener('click', function(e) {
        // 向上查找是否点击了 <a> 标签（处理点击链接内部图标/文字的情况）
        const link = e.target.closest('a');

        // 如果是链接且以 magnet: 开头
        if (link && link.href.startsWith('magnet:')) {
            // 1. 阻止默认行为（防止系统弹出 "打开 xxxx 应用程序" 的提示）
            e.preventDefault();
            e.stopPropagation();

            const magnetUrl = link.href;

            // 2. 复制链接到剪贴板
            // 使用 GM_setClipboard 以确保兼容性最好
            GM_setClipboard(magnetUrl, 'text');

            // 3. 在新标签页打开目标地址
            // 使用 GM_openInTab 可以更灵活控制新标签页行为 (false 表示不要在后台打开，即立即切换过去)
            GM_openInTab(TARGET_URL, { active: true });

            console.log(`[Magnet Helper] Copied: ${magnetUrl.substring(0, 20)}...`);
        }
    }, true); // 使用捕获阶段 (true) 以确保在其他脚本之前拦截
})();
