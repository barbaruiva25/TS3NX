// Hooks temporarios de boot: acham qual init da CRT retorna 0 e faz o jogo
// sair logo no entry (thread guest retorna em ms; "Execution complete").
// Cada entrada diz o que investiga; remover quando a causa estiver corrigida.
// Padrao: REX_HOOK_RAW troca a funcao guest; __imp__ chama o original.

#include <rex/hook.h>
#include <rex/logging.h>

// INVESTIGACAO (boot-010, 14/10/2026): o entry 0x88F12800 nao tem DEFINE
// proprio (fundido no corpo de sub_88F126A8), entao hook nele e codigo morto.
// O redirect vai no 88F126A8, que dispara como entry real. Origem: mesma
// logica do default.xex (args zerados -> ord 3).
REX_EXTERN(__imp__sub_88F126A8);
REX_EXTERN(__imp__sub_88329E10);
REX_EXTERN(__imp__sub_88329E08);
REX_HOOK_RAW(sub_88F126A8) {
  // O SDK nao zera o contexto do thread (r4-r12, CR etc. sao lixo do host,
  // nao-deterministico entre boots). HW/Xenia zeram: replica aqui, preservando
  // r1 (stack), r3 (start_context) e r13 (PCR), antes de qualquer codigo guest.
  ctx.r4.u64 = 0; ctx.r5.u64 = 0; ctx.r6.u64 = 0; ctx.r7.u64 = 0;
  ctx.r8.u64 = 0; ctx.r9.u64 = 0; ctx.r10.u64 = 0; ctx.r11.u64 = 0;
  ctx.r12.u64 = 0;
  ctx.r14.u64 = 0; ctx.r15.u64 = 0; ctx.r16.u64 = 0; ctx.r17.u64 = 0;
  ctx.r18.u64 = 0; ctx.r19.u64 = 0; ctx.r20.u64 = 0; ctx.r21.u64 = 0;
  ctx.r22.u64 = 0; ctx.r23.u64 = 0; ctx.r24.u64 = 0; ctx.r25.u64 = 0;
  ctx.r26.u64 = 0; ctx.r27.u64 = 0; ctx.r28.u64 = 0; ctx.r29.u64 = 0;
  ctx.r30.u64 = 0; ctx.r31.u64 = 0;
  ctx.cr0.lt = ctx.cr0.gt = ctx.cr0.eq = ctx.cr0.so = 0;
  ctx.cr1.lt = ctx.cr1.gt = ctx.cr1.eq = ctx.cr1.so = 0;
  ctx.cr2.lt = ctx.cr2.gt = ctx.cr2.eq = ctx.cr2.so = 0;
  ctx.cr3.lt = ctx.cr3.gt = ctx.cr3.eq = ctx.cr3.so = 0;
  ctx.cr4.lt = ctx.cr4.gt = ctx.cr4.eq = ctx.cr4.so = 0;
  ctx.cr5.lt = ctx.cr5.gt = ctx.cr5.eq = ctx.cr5.so = 0;
  ctx.cr6.lt = ctx.cr6.gt = ctx.cr6.eq = ctx.cr6.so = 0;
  ctx.cr7.lt = ctx.cr7.gt = ctx.cr7.eq = ctx.cr7.so = 0;
  ctx.xer.so = 0; ctx.xer.ov = 0; ctx.xer.ca = 0;
  ctx.ctr.u64 = 0;
  // Ordem do privloader: ord 2 (r3=1, arma [0x892F3FA0]) e so depois ord 3
  // (r3=launch data, r4=1020 + residuos).
  ctx.r3.u32 = 1;
  __imp__sub_88329E08(ctx, base);
  REXLOG_WARN("[dbg] ord2 retornou r3={:08X}", ctx.r3.u32);
  // r4 = 1020). Residuos exatos emulados do memset do priv (0x82013190) +
  // preservacao pelo kernel (so escreve r3): r5=1016, r6=fim do buffer,
  // r7=0. r6 precisa ser legivel (88352FC0 le [r6],[r6+4]): zeros controlados.
  const uint32_t buf = (ctx.r1.u32 - 0xC00u) & ~3u;
  for (uint32_t i = 0; i < 1032; i++) base[buf + i] = 0;
  ctx.r3.u32 = buf;
  ctx.r4.u32 = 1020;
  ctx.r5.u32 = 1016;
  ctx.r6.u32 = buf + 1024;
  ctx.r7.u32 = 0;
  // Sonda: check cmplw r31,r26 em 88352FC0 exige r31 < r26.
  // E cmplwi r8,2 em 88353090 exige r8 de entrada >= 2 (r8 so e recarregado
  // depois; com r8<2 o loop externo nunca avanca -> -1).
  ctx.r26.u32 = 0x1000;
  ctx.r31.u32 = 8;
  ctx.r8.u32 = 2;
  REXLOG_WARN("[dbg] entry->ord3 0x88329E10 (buf {:08X}, residuos priv)", buf);
  __imp__sub_88329E10(ctx, base);
  REXLOG_WARN("[dbg] ord3 retornou r3={:08X}", ctx.r3.u32);
}

REX_EXTERN(__imp__sub_8833BBC0);
REX_HOOK_RAW(sub_8833BBC0) {
  REXLOG_WARN("[dbg] IN sub_8833BBC0 r3={:08X} r4={:08X} lr={:08X}", ctx.r3.u32, ctx.r4.u32,
              static_cast<uint32_t>(ctx.lr));
  __imp__sub_8833BBC0(ctx, base);
  REXLOG_WARN("[dbg] OUT sub_8833BBC0 r3={:08X}", ctx.r3.u32);
}

REX_EXTERN(__imp__sub_88352FC0);
REX_HOOK_RAW(sub_88352FC0) {
  REXLOG_WARN("[dbg] IN sub_88352FC0 r3={:08X} r4={:08X} lr={:08X}", ctx.r3.u32, ctx.r4.u32,
              static_cast<uint32_t>(ctx.lr));
  __imp__sub_88352FC0(ctx, base);
  REXLOG_WARN("[dbg] OUT sub_88352FC0 r3={:08X}", ctx.r3.u32);
}

REX_EXTERN(__imp__sub_885CD568);
REX_HOOK_RAW(sub_885CD568) {
  REXLOG_WARN("[dbg] IN sub_885CD568 r3={:08X} r4={:08X} lr={:08X}", ctx.r3.u32, ctx.r4.u32,
              static_cast<uint32_t>(ctx.lr));
  __imp__sub_885CD568(ctx, base);
  REXLOG_WARN("[dbg] OUT sub_885CD568 r3={:08X}", ctx.r3.u32);
}

REX_EXTERN(__imp__sub_88328320);
REX_HOOK_RAW(sub_88328320) {
  REXLOG_WARN("[dbg] IN sub_88328320 r3={:08X} r4={:08X} lr={:08X}", ctx.r3.u32, ctx.r4.u32,
              static_cast<uint32_t>(ctx.lr));
  __imp__sub_88328320(ctx, base);
  REXLOG_WARN("[dbg] OUT sub_88328320 r3={:08X}", ctx.r3.u32);
}

REX_EXTERN(__imp__sub_8840C898);
REX_HOOK_RAW(sub_8840C898) {
  REXLOG_WARN("[dbg] IN sub_8840C898 r3={:08X} r4={:08X} lr={:08X}", ctx.r3.u32, ctx.r4.u32,
              static_cast<uint32_t>(ctx.lr));
  __imp__sub_8840C898(ctx, base);
  REXLOG_WARN("[dbg] OUT sub_8840C898 r3={:08X}", ctx.r3.u32);
}

REX_EXTERN(__imp__sub_883289C8);
REX_HOOK_RAW(sub_883289C8) {
  REXLOG_WARN("[dbg] IN sub_883289C8 r3={:08X} r4={:08X} lr={:08X}", ctx.r3.u32, ctx.r4.u32,
              static_cast<uint32_t>(ctx.lr));
  __imp__sub_883289C8(ctx, base);
  REXLOG_WARN("[dbg] OUT sub_883289C8 r3={:08X}", ctx.r3.u32);
}

REX_EXTERN(__imp__sub_88329718);
REX_HOOK_RAW(sub_88329718) {
  REXLOG_WARN("[dbg] IN sub_88329718 r3={:08X} r4={:08X} lr={:08X}", ctx.r3.u32, ctx.r4.u32,
              static_cast<uint32_t>(ctx.lr));
  __imp__sub_88329718(ctx, base);
  REXLOG_WARN("[dbg] OUT sub_88329718 r3={:08X}", ctx.r3.u32);
}

// Se o entry retornar, estes 4 inits sao os suspeitos (cadeia sub_88F12508).
REX_EXTERN(__imp__sub_88F3BFE0);
REX_HOOK_RAW(sub_88F3BFE0) {
  REXLOG_WARN("[dbg] IN sub_88F3BFE0 lr={:08X}", static_cast<uint32_t>(ctx.lr));
  __imp__sub_88F3BFE0(ctx, base);
  REXLOG_WARN("[dbg] OUT sub_88F3BFE0 r3={:08X}", ctx.r3.u32);
}

REX_EXTERN(__imp__sub_88F20A18);
REX_HOOK_RAW(sub_88F20A18) {
  REXLOG_WARN("[dbg] IN sub_88F20A18 lr={:08X}", static_cast<uint32_t>(ctx.lr));
  __imp__sub_88F20A18(ctx, base);
  REXLOG_WARN("[dbg] OUT sub_88F20A18 r3={:08X}", ctx.r3.u32);
}

REX_EXTERN(__imp__sub_88F3BF08);
REX_HOOK_RAW(sub_88F3BF08) {
  REXLOG_WARN("[dbg] IN sub_88F3BF08 lr={:08X}", static_cast<uint32_t>(ctx.lr));
  __imp__sub_88F3BF08(ctx, base);
  REXLOG_WARN("[dbg] OUT sub_88F3BF08 r3={:08X}", ctx.r3.u32);
}

REX_EXTERN(__imp__sub_88F3BE28);
REX_HOOK_RAW(sub_88F3BE28) {
  REXLOG_WARN("[dbg] IN sub_88F3BE28 lr={:08X}", static_cast<uint32_t>(ctx.lr));
  __imp__sub_88F3BE28(ctx, base);
  REXLOG_WARN("[dbg] OUT sub_88F3BE28 r3={:08X}", ctx.r3.u32);
}
