// 标准写法问号(圆钩 + 直尾)的中心线,输出 {hook, dot}(字体单位,SVG 坐标 y 向下),即 index.html 里的 QDATA。
// 用法:node probe/question_std.js
// 设计坐标 y 向上:钩是以 (CX, CY) 为圆心、半径 R 的圆弧,从 A0° 顺时针转到 A1°;再用一段三次曲线收到中线 x = CX,
// 直线向下到 STEM_END;圆点圆心在 (CX, DOT_Y)。笔宽不在这里,渲染时与正文相同。
const CX = 870, CY = 1500, R = 360, A0 = 170, A1 = -40, STEM_TOP = 1000, STEM_END = 720, DOT_Y = 150, K1 = .55, K2 = .45;
const rad = d => d * Math.PI / 180, F = p => `${Math.round(p[0])} ${Math.round(-p[1])}`;
const P = a => [CX + R * Math.cos(rad(a)), CY + R * Math.sin(rad(a))], T = a => [Math.sin(rad(a)), -Math.cos(rad(a))];   // T:顺时针切线
let d = `M${F(P(A0))}`;
const n = Math.ceil((A0 - A1) / 90), step = (A0 - A1) / n, k = 4 / 3 * Math.tan(rad(step) / 4) * R;   // 每段不超过 90° 的圆弧贝塞尔近似
for (let i = 0; i < n; i++) {
  const s = A0 - i * step, e = s - step, ps = P(s), pe = P(e), ts = T(s), te = T(e);
  d += `C${F([ps[0] + ts[0] * k, ps[1] + ts[1] * k])} ${F([pe[0] - te[0] * k, pe[1] - te[1] * k])} ${F(pe)}`;
}
const pe = P(A1), te = T(A1), gap = Math.hypot(CX - pe[0], STEM_TOP - pe[1]);
d += `C${F([pe[0] + te[0] * gap * K1, pe[1] + te[1] * gap * K1])} ${F([CX, STEM_TOP + gap * K2])} ${F([CX, STEM_TOP])}`;
const L = STEM_TOP - STEM_END;
d += `C${F([CX, STEM_TOP - L / 3])} ${F([CX, STEM_TOP - 2 * L / 3])} ${F([CX, STEM_END])}`;
console.log(JSON.stringify({ hook: d, dot: [CX, -DOT_Y] }));
