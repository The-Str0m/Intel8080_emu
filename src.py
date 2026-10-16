#include <iostream>
#include <stdint.h>
#include <fstream>
uint8_t memory[0x10000];
void out_port(uint8_t port, uint8_t value){}
void in_port(uint8_t port, uint8_t value){}
void loadROM(const std::string& filename, uint16_t startadress){
    std::ifstream rom(filename, std::ios::binary | std::ios::ate);
    std::streamsize size = rom.tellg();
    rom.seekg(0, std::ios::beg);
    rom.read(reinterpret_cast<char*>(&memory[startadress]), size);
    rom.close();
}

int main(){
    uint8_t A = 0, B = 0, C = 0, D = 0, E = 0, H = 0, L = 0;
    uint16_t sp = 0;
    uint16_t pc = 0;
    uint8_t flag = 0;
    uint8_t default_flag = 0x02;

    //load roms

    loadROM("invaders.e", 0x0000);
    loadROM("invaders.f", 0x1000);
    loadROM("invaders.g", 0x2000);
    loadROM("invaders.h", 0x3000);
    pc = 0x0000;

    bool running = true;
    bool interrupt_enabled = false;

    while(running){
        uint8_t opcode = memory[pc];

        switch(opcode){
            case 0x00: {
                pc += 1;
                break;
            }
            case 0x01: {
                C = memory[pc+1];
                B = memory[pc+2];
                pc += 3;
                break;
            }
            case 0x02: {
                memory[B<<8|C] = A;
                pc += 1;
                break;
            }
            case 0x03: {
                uint16_t BC = (B << 8) | C;
                BC += 1;
                B = (BC >> 8) & 0xFF;
                C = BC & 0xFF;
                pc += 1;
                break;
            }
            case 0x04: {
                flag = (flag & 0x01) | default_flag;
                if((B&0x0F)+1>0x0F){
                    flag |= 0x10;
                }
                B += 1;
                if(B==0){
                    flag |= 0x40;
                }
                if((B >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(B)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x05: {
                flag = (flag & 0x01) | default_flag;
                if((B&0x0F)==0){
                    flag |= 0x10;
                }
                B -= 1;
                if(B==0){
                    flag |= 0x40;
                }
                if((B >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(B)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x06: {
                B = memory[pc+1];
                pc += 2;
                break;
            }
            case 0x07: {
                uint8_t carry = A >> 7;
                A = (A << 1) | carry;
                flag = (flag & 0xFE) | carry;
                pc += 1;
                break;
            }
            case 0x08: {
                printf("0x08");
                running = false;
                break;
            }
            case 0x09: {
                uint16_t HL = (H << 8) | L;
                uint16_t BC = (B << 8) | C;
                uint32_t total = HL + BC;
                if(total & 0x10000){
                    flag |= 0x01;
                }
                else{
                    flag &= ~0x01;
                }
                H = total >> 8 & 0xFF;
                L = total & 0xFF;
                pc += 1;
                break;
            }
            case 0x0A: {
                A = memory[(B << 8)|C];
                pc += 1;
                break;
            }
            case 0x0B: {
                uint16_t BC = (B << 8) | C;
                BC -= 1;
                B = (BC >> 8) & 0xFF;
                C = BC & 0xFF;
                pc += 1;
                break;
            }
            case 0x0C: {
                flag = (flag & 0x01) | default_flag;
                if((C&0x0F)+1>0x0F){
                    flag |= 0x10;
                }
                C += 1;
                if(C==0){
                    flag |= 0x40;
                }
                if((C >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(C)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x0D: {
                flag = (flag & 0x01) | default_flag;
                if((C&0x0F)==0){
                    flag |= 0x10;
                }
                C -= 1;
                if(C==0){
                    flag |= 0x40;
                }
                if((C >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(C)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x0E: {
                C = memory[pc+1];
                pc += 2;
                break;
            }
            case 0x0F: {
                uint8_t carry = A & 0x01;
                if(carry){
                    A = A >> 1 | 0x80;
                }
                else{
                    A >>= 1;
                }
                flag = (flag & 0xFE) | carry;
                pc += 1;
                break;
            }
            case 0x10: {
                printf("0x10");
                running = false;
                break;
            }
            case 0x11: {
                E = memory[pc+1];
                D = memory[pc+2];
                pc += 3;
                break;
            }
            case 0x12: {
                memory[D<<8|E] = A;
                pc += 1;
                break;
            }
            case 0x13: {
                uint16_t DE = (D << 8) | E;
                DE += 1;
                D = (DE >> 8) & 0xFF;
                E = DE & 0xFF;
                pc += 1;
                break;
            }
            case 0x14: {
                flag = (flag & 0x01) | default_flag;
                if((D&0x0F)+1>0x0F){
                    flag |= 0x10;
                }
                D += 1;
                if(D==0){
                    flag |= 0x40;
                }
                if((D >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(D)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x15: {
                flag = (flag & 0x01) | default_flag;
                if((D&0x0F)==0){
                    flag |= 0x10;
                }
                D -= 1;
                if(D==0){
                    flag |= 0x40;
                }
                if((D >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(D)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x16: {
                D = memory[pc+1];
                pc += 2;
                break;
            }
            case 0x17: {
                uint8_t carry = A >> 7;
                if(flag&0x01){
                    A  = (A << 1) | 0x01;
                }
                else{
                    A <<= 1;
                }
                flag = (flag & 0xFE) | carry;
                pc += 1;
                break;
            }
            case 0x18: {
                printf("0x18");
                running = false;
                break;
            }
            case 0x19: {
                uint16_t HL = (H << 8) | L;
                uint16_t DE = (D << 8) | E;
                uint32_t total = HL + DE;
                if(total & 0x10000){
                    flag |= 0x01;
                }
                else{
                    flag &= ~0x01;
                }
                H = total >> 8 & 0xFF;
                L = total & 0xFF;
                pc += 1;
                break;
            }
            case 0x1A: {
                A = memory[(D << 8)|E];
                pc += 1;
                break;
            }
            case 0x1B: {
                uint16_t DE = (D << 8) | E;
                DE -= 1;
                D = (DE >> 8) & 0xFF;
                E = DE & 0xFF;
                pc += 1;
                break;
            }
            case 0x1C: {
                flag = (flag & 0x01) | default_flag;
                if((E&0x0F)+1>0x0F){
                    flag |= 0x10;
                }
                E += 1;
                if(E==0){
                    flag |= 0x40;
                }
                if((E >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(E)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x1D: {
                flag = (flag & 0x01) | default_flag;
                if((E&0x0F)==0){
                    flag |= 0x10;
                }
                E -= 1;
                if(E==0){
                    flag |= 0x40;
                }
                if((E >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(E)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x1E: {
                E = memory[pc+1];
                pc += 2;
                break;
            }
            case 0x1F: {
                uint8_t carry = A & 0x01;
                if(flag & 0x01){
                    A  = (A >> 1) | 0x80;
                }
                else{
                    A >>= 1;
                }
                flag = (flag & 0xFE) | carry;
                pc += 1;
                break;
            }
            case 0x20: {
                printf("0x20");
                running = false;
                break;
            }
            case 0x21: {
                L = memory[pc+1];
                H = memory[pc+2];
                pc += 3;
                break;
            }
            case 0x22: {
                memory[(memory[pc+1]|(memory[pc+2]<<8))] = L;
                memory[(memory[pc+1]|(memory[pc+2]<<8))+1] = H;
                pc += 3;
                break;
            }
            case 0x23: {
                uint16_t HL = (H << 8) | L;
                HL += 1;
                H = (HL >> 8) & 0xFF;
                L = HL & 0xFF;
                pc += 1;
                break;
            }
            case 0x24: {
                flag = (flag & 0x01) | default_flag;
                if((H&0x0F)+1>0x0F){
                    flag |= 0x10;
                }
                H += 1;
                if(H==0){
                    flag |= 0x40;
                }
                if((H >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(H)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x25: {
                flag = (flag & 0x01) | default_flag;
                if((H&0x0F)==0){
                    flag |= 0x10;
                }
                H -= 1;
                if(H==0){
                    flag |= 0x40;
                }
                if((H >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(H)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x26: {
                H = memory[pc+1];
                pc += 2;
                break;
            }
            case 0x27: {
                uint8_t correction = 0;
                uint8_t ac = 0, cy = flag & 0x01;
                if((A & 0x0F) > 9 || (flag & 0x10)) {
                    correction += 0x06;
                    ac = 0x10;
                }
                uint16_t result = A + correction;
                if (((result & 0xF0) > 0x90) || cy) {
                    correction += 0x60;
                    cy = 0x01;
                }
                A += correction;
                flag = default_flag;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A) % 2)){
                    flag |= 0x04;
                }
                if(ac){
                    flag |= 0x10;
                }
                if(cy){
                    flag |= 0x01;
                }
                pc += 1;
                break;
            }
            case 0x28: {
                printf("0x28");
                running = false;
                break;
            }
            case 0x29: {
                uint16_t HL = (H << 8) | L;
                uint32_t total = HL + HL;
                if(total & 0x10000){
                    flag |= 0x01;
                }
                else{
                    flag &= ~0x01;
                }
                H = total >> 8 & 0xFF;
                L = total & 0xFF;
                pc += 1;
                break;
            }
            case 0x2A: {
                L = memory[memory[pc+1]|(memory[pc+2]<<8)];
                H = memory[(memory[pc+1]|(memory[pc+2]<<8))+1];
                pc += 3;
                break;
            }
            case 0x2B: {
                uint16_t HL = (H << 8) | L;
                HL -= 1;
                H = (HL >> 8) & 0xFF;
                L = HL & 0xFF;
                pc += 1;
                break;
            }
            case 0x2C: {
                flag = (flag & 0x01) | default_flag;
                if((L&0x0F)+1>0x0F){
                    flag |= 0x10;
                }
                L += 1;
                if(L==0){
                    flag |= 0x40;
                }
                if((L >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(L)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x2D: {
                flag = (flag & 0x01) | default_flag;
                if((L&0x0F)==0){
                    flag |= 0x10;
                }
                L -= 1;
                if(L==0){
                    flag |= 0x40;
                }
                if((L >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(L)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }               
            case 0x2E: {
                L = memory[pc+1];
                pc += 2;
                break;
            }
            case 0x2F: {
                A = ~A;
                pc += 1;
                break;
            }
            case 0x30: {
                printf("0x30");
                running = false;
                break;
            }
            case 0x31: {
                sp = memory[pc+1] | memory[pc+2] << 8;
                pc += 3;
                break;
            }
            case 0x32: {
                memory[memory[pc+2]<<8|memory[pc+1]] = A;
                pc += 3;
                break;
            }
            case 0x33: {
                sp += 1;
                pc += 1;
                break;
            }
            case 0x34: {
                uint8_t M = memory[H<<8|L];
                flag = (flag & 0x01) | default_flag;
                if((M&0x0F)+1>0x0F){
                    flag |= 0x10;
                }
                M += 1;
                memory[H<<8|L] = M;
                if(M==0){
                    flag |= 0x40;
                }
                if((M >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(M)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x35: {
                flag = (flag & 0x01) | default_flag;
                uint8_t M = memory[H<<8|L];
                if((M&0x0F)==0){
                    flag |= 0x10;
                }
                M -= 1;
                if(M==0){
                    flag |= 0x40;
                }
                if((M >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(M)%2)){
                    flag |= 0x04;
                }
                memory[H<<8|L] = M;
                pc += 1;
                break;
            }
            case 0x36: {
                memory[H<<8|L] = memory[pc+1];
                pc += 2;
                break;
            }
            case 0x37: {
                flag |= 0x01;
                pc += 1;
                break;
            }
            case 0x38: {
                printf("0x38");
                running = false;
                break;
            }
            case 0x39: {
                uint16_t HL = (H << 8) | L;
                uint32_t total = HL + sp;
                if(total & 0x10000){
                    flag |= 0x01;
                }
                else{
                    flag &= ~0x01;
                }
                H = total >> 8 & 0xFF;
                L = total & 0xFF;
                pc += 1;
                break;
            }
            case 0x3A: {
                A = memory[memory[pc+2] << 8 | memory[pc+1]];
                pc += 3;
                break;
            }
            case 0x3B: {
                sp -= 1;
                pc += 1;
                break;
            }
            case 0x3C: {
                flag = (flag & 0x01) | default_flag;
                if((A&0x0F)+1>0x0F){
                    flag |= 0x10;
                }
                A += 1;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x3D: {
                flag = (flag & 0x01) | default_flag;
                if((A&0x0F)==0){
                    flag |= 0x10;
                }
                A -= 1;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x3E: {
                A = memory[pc+1];
                pc += 2;
                break;
            }
            case 0x3F: {
                if(flag & 0x01){
                    flag &= 0xFE;
                }
                else{
                    flag |= 0x01;
                }
                pc += 1;
                break;
            }
            case 0x40: {
                pc += 1;
                break;
            }
            case 0x41: {
                B = C;
                pc += 1;
                break;
            }
            case 0x42: {
                B = D;
                pc += 1;
                break;
            }
            case 0x43: {
                B = E;
                pc += 1;
                break;
            }
            case 0x44: {
                B = H;
                pc += 1;
                break;
            }
            case 0x45: {
                B = L;
                pc += 1;
                break;
            }
            case 0x46: {
                B = memory[H<<8|L];
                pc += 1;
                break;
            }
            case 0x47: {
                B = A;
                pc += 1;
                break;
            }
            case 0x48: {
                C = B;
                pc += 1;
                break;
            }
            case 0x49: {
                pc += 1;
                break;
            }
            case 0x4A: {
                C = D;
                pc += 1;
                break;
            }
            case 0x4B: {
                C = E;
                pc += 1;
                break;
            }
            case 0x4C: {
                C = H;
                pc += 1;
                break;
            }
            case 0x4D: {
                C = L;
                pc += 1;
                break;
            }
            case 0x4E: {
                C = memory[H<<8|L];
                pc += 1;
                break;
            }
            case 0x4F: {
                C = A;
                pc += 1;
                break;
            }
            case 0x50: {
                D = B;
                pc += 1;
                break;
            }
            case 0x51: {
                D = C;
                pc += 1;
                break;
            }
            case 0x52: {
                pc += 1;
                break;
            }
            case 0x53: {
                D = E;
                pc += 1;
                break;
            }
            case 0x54: {
                D = H;
                pc += 1;
                break;
            }
            case 0x55: {
                D = L;
                pc += 1;
                break;
            }
            case 0x56: {
                D = memory[H<<8|L];
                pc += 1;
                break;
            }
            case 0x57: {
                D = A;
                pc += 1;
                break;
            }
            case 0x58: {
                E = B;
                pc += 1;
                break;
            }
            case 0x59: {
                E = C;
                pc += 1;
                break;
            }
            case 0x5A: {
                E = D;
                pc += 1;
                break;
            }
            case 0x5B: {
                pc += 1;
                break;
            }
            case 0x5C: {
                E = H;
                pc += 1;
                break;
            }
            case 0x5D: {
                E = L;
                pc += 1;
                break;
            }
            case 0x5E: {
                E = memory[H<<8|L];
                pc += 1;
                break;
            }
            case 0x5F: {
                E = A;
                pc += 1;
                break;
            }
            case 0x60: {
                H = B;
                pc += 1;
                break;
            }
            case 0x61: {
                H = C;
                pc += 1;
                break;
            }
            case 0x62: {
                H = D;
                pc += 1;
                break;
            }
            case 0x63: {
                H = E;
                pc += 1;
                break;
            }
            case 0x64: {
                H = H;
                pc += 1;
                break;
            }
            case 0x65: {
                H = L;
                pc += 1;
                break;
            }
            case 0x66: {
                H = memory[H<<8|L];
                pc += 1;
                break;
            }
            case 0x67: {
                H = A;
                pc += 1;
                break;
            }
            case 0x68: {
                L = B;
                pc += 1;
                break;
            }
            case 0x69: {
                L = C;
                pc += 1;
                break;
            }
            case 0x6A: {
                L = D;
                pc += 1;
                break;
            }
            case 0x6B: {
                L = E;
                pc += 1;
                break;
            }
            case 0x6C: {
                L = H;
                pc += 1;
                break;
            }
            case 0x6D: {
                L = L;
                pc += 1;
                break;
            }
            case 0x6E: {
                L = memory[H<<8|L];
                pc += 1;
                break;
            }
            case 0x6F: {
                L = A;
                pc += 1;
                break;
            }
            case 0x70: {
                memory[H<<8|L] = B;
                pc += 1;
                break;
            }
            case 0x71: {
                memory[H<<8|L] = C;
                pc += 1;
                break;
            }
            case 0x72: {
                memory[H<<8|L] = D;
                pc += 1;
                break;
            }
            case 0x73: {
                memory[H<<8|L] = E;
                pc += 1;
                break;
            }
            case 0x74: {
                memory[H<<8|L] = H;
                pc += 1;
                break;
            }
            case 0x75: {
                memory[H<<8|L] = L;
                pc += 1;
                break;
            }
            case 0x76: {
                running = false;
                pc += 1;
                break;
            }
            case 0x77: {
                memory[H<<8|L] = A;
                pc += 1;
                break;
            }
            case 0x78: {
                A = B;
                pc += 1;
                break;
            }
            case 0x79: {
                A = C;
                pc += 1;
                break;
            }
            case 0x7A: {
                A = D;
                pc += 1;
                break;
            }
            case 0x7B: {
                A = E;
                pc += 1;
                break;
            }
            case 0x7C: {
                A = H;
                pc += 1;
                break;
            }
            case 0x7D: {
                A = L;
                pc += 1;
                break;
            }
            case 0x7E: {
                A = memory[H<<8|L];
                pc += 1;
                break;
            }
            case 0x7F: {
                pc += 1;
                break;
            }
            case 0x80: {
                flag = default_flag;
                if((A&0x0F)+(B&0x0F)>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A + B;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x81: {
                flag = default_flag;
                if((A&0x0F)+(C&0x0F)>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A + C;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x82: {
                flag = default_flag;
                if((A&0x0F)+(D&0x0F)>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A + D;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x83: {
                flag = default_flag;
                if((A&0x0F)+(E&0x0F)>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A + E;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x84: {
                flag = default_flag;
                if((A&0x0F)+(H&0x0F)>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A + H;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x85: {
                flag = default_flag;
                if((A&0x0F)+(L&0x0F)>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A + L;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x86: {
                uint8_t M = memory[H<<8|L];
                flag = default_flag;
                if((A&0x0F)+(M&0x0F)>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A + M;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x87: {
                flag = default_flag;
                if((A&0x0F)+(A&0x0F)>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A + A;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x88: {
                uint8_t c = flag&0x01;
                flag = default_flag;
                if((A&0x0F)+(B&0x0F)+c>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A+B+c;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x89: {
                uint8_t c = flag&0x01;
                flag = default_flag;
                if((A&0x0F)+(C&0x0F)+c>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A+C+c;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x8A: {
                uint8_t c = flag&0x01;
                flag = default_flag;
                if((A&0x0F)+(D&0x0F)+c>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A+D+c;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x8B: {
                uint8_t c = flag&0x01;
                flag = default_flag;
                if((A&0x0F)+(E&0x0F)+c>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A+E+c;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x8C: {
                uint8_t c = flag&0x01;
                flag = default_flag;
                if((A&0x0F)+(H&0x0F)+c>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A+H+c;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x8D: {
                uint8_t c = flag&0x01;
                flag = default_flag;
                if((A&0x0F)+(L&0x0F)+c>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A+L+c;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x8E: {
                uint8_t M = memory[H << 8 | L];
                uint8_t c = flag&0x01;
                flag = default_flag;
                if((A&0x0F)+(M&0x0F)+c>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A+M+c;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x8F: {
                uint8_t c = flag&0x01;
                flag = default_flag;
                if((A&0x0F)+(A&0x0F)+c>0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A+A+c;
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A==0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x90: {
                flag = default_flag;
                if((A & 0x0F) < (B & 0x0F)) {
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~B) + 1;
                if(A<B){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x91: {
                flag = default_flag;
                if((A & 0x0F) < (C & 0x0F)) {
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~C) + 1;
                if(A<C){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x92: {
                flag = default_flag;
                if((A & 0x0F) < (D & 0x0F)) {
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~D) + 1;
                if(A<D){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x93: {
                flag = default_flag;
                if((A & 0x0F) < (E & 0x0F)) {
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~E) + 1;
                if(A<E){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x94: {
                flag = default_flag;
                if((A & 0x0F) < (H & 0x0F)) {
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~H) + 1;
                if(A<H){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x95: {
                flag = default_flag;
                if((A & 0x0F) < (L & 0x0F)) {
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~L) + 1;
                if(A<L){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x96: {
                uint8_t M = memory[H << 8 | L];
                flag = default_flag;
                if((A & 0x0F) < (M & 0x0F)) {
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~M) + 1;
                if(A<M){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x97: {
                flag = default_flag;
                A = 0;
                flag |= 0x40;
                flag |= 0x10;
                if (!(__builtin_popcount(A) % 2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x98: {
                uint8_t cy = flag&0x01;
                uint16_t temp_reg = B+cy;
                flag = default_flag;
                if((A & 0x0F) < ((B & 0x0F)+cy)){
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~temp_reg) + 1;
                if(A < temp_reg){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x99: {
                uint8_t cy = flag&0x01;
                uint16_t temp_reg = C+cy;
                flag = default_flag;
                if((A & 0x0F) < ((C & 0x0F)+cy)){
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~temp_reg) + 1;
                if(A < temp_reg){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x9A: {
                uint8_t cy = flag&0x01;
                uint16_t temp_reg = D+cy;
                flag = default_flag;
                if((A & 0x0F) < ((D & 0x0F)+cy)){
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~temp_reg) + 1;
                if(A < temp_reg){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x9B: {
                uint8_t cy = flag&0x01;
                uint16_t temp_reg = E+cy;
                flag = default_flag;
                if((A & 0x0F) < ((E & 0x0F)+cy)){
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~temp_reg) + 1;
                if(A < temp_reg){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x9C: {
                uint8_t cy = flag&0x01;
                uint16_t temp_reg = H+cy;
                flag = default_flag;
                if((A & 0x0F) < ((H & 0x0F)+cy)){
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~temp_reg) + 1;
                if(A < temp_reg){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x9D: {
                uint8_t cy = flag&0x01;
                uint16_t temp_reg = L+cy;
                flag = default_flag;
                if((A & 0x0F) < ((L & 0x0F)+cy)){
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~temp_reg) + 1;
                if(A < temp_reg){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x9E: {
                uint8_t M = memory[H<<8|L];
                uint8_t cy = flag&0x01;
                uint16_t temp_reg = M+cy;
                flag = default_flag;
                if((A & 0x0F) < ((M & 0x0F)+cy)){
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~temp_reg) + 1;
                if(A < temp_reg){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0x9F: {
                uint8_t cy = flag&0x01;
                uint16_t temp_reg = A+cy;
                flag = default_flag;
                if((A & 0x0F) < ((A & 0x0F)+cy)){
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~temp_reg) + 1;
                if(A < temp_reg){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if((A >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xA0: {
                flag = default_flag & ~0x01;
                flag |= 0x10;
                A &= B;
                if(A==0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xA1: {
                flag = default_flag & ~0x01;
                flag |= 0x10;
                A &= C;
                if(A==0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xA2: {
                flag = default_flag & ~0x01;
                flag |= 0x10;
                A &= D;
                if(A==0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xA3: {
                flag = default_flag & ~0x01;
                flag |= 0x10;
                A &= E;
                if(A==0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xA4: {
                flag = default_flag & ~0x01;
                flag |= 0x10;
                A &= H;
                if(A==0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xA5: {
                flag = default_flag & ~0x01;
                flag |= 0x10;
                A &= L;
                if(A==0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xA6: {
                uint8_t M = memory[H << 8|L];
                flag = default_flag & ~0x01;
                flag |= 0x10;
                A &= M;
                if(A==0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xA7: {
                flag = default_flag & ~0x01;
                flag |= 0x10;
                A &= A;
                if(A==0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xA8: {
                flag = default_flag;
                A ^= B;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xA9: {
                flag = default_flag;
                A ^= C;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xAA: {
                flag = default_flag;
                A ^= D;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xAB: {
                flag = default_flag;
                A ^= E;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xAC: {
                flag = default_flag;
                A ^= H;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xAD: {
                flag = default_flag;
                A ^= L;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xAE: {
                flag = default_flag;
                uint8_t M = memory[H << 8 | L];
                A ^= M;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xAF: {
                flag = default_flag;
                A ^= A;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xB0: {
                flag = default_flag;
                A |= B;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xB1: {
                flag = default_flag;
                A |= C;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xB2: {
                flag = default_flag;
                A |= D;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xB3: {
                flag = default_flag;
                A |= E;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xB4: {
                flag = default_flag;
                A |= H;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xB5: {
                flag = default_flag;
                A |= L;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xB6: {
                flag = default_flag;
                uint8_t M = memory[ H << 8 | L];
                A |= M;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xB7: {
                flag = default_flag;
                A |= A;
                if(A == 0){
                    flag |= 0x40;
                }
                if(A>>7&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xB8: {
                flag = default_flag;
                if((A & 0x0F) < (B & 0x0F)) {
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~B) + 1;
                if(!(sum > 0xFF)){
                    flag |= 0x01;
                }
                sum &= 0xFF;
                if(sum == 0){
                    flag |= 0x40;
                }
                if((sum >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(sum)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xB9: {
                flag = default_flag;
                if((A & 0x0F) < (C & 0x0F)) {
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~C) + 1;
                if(!(sum > 0xFF)){
                    flag |= 0x01;
                }
                sum &= 0xFF;
                if(sum == 0){
                    flag |= 0x40;
                }
                if((sum >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(sum)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xBA: {
                flag = default_flag;
                if((A & 0x0F) < (D & 0x0F)) {
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~D) + 1;
                if(!(sum > 0xFF)){
                    flag |= 0x01;
                }
                sum &= 0xFF;
                if(sum == 0){
                    flag |= 0x40;
                }
                if((sum >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(sum)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xBB: {
                flag = default_flag;
                if((A & 0x0F) < (E & 0x0F)) {
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~E) + 1;
                if(!(sum > 0xFF)){
                    flag |= 0x01;
                }
                sum &= 0xFF;
                if(sum == 0){
                    flag |= 0x40;
                }
                if((sum >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(sum)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xBC: {
                flag = default_flag;
                if((A & 0x0F) < (H & 0x0F)) {
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~H) + 1;
                if(!(sum > 0xFF)){
                    flag |= 0x01;
                }
                sum &= 0xFF;
                if(sum == 0){
                    flag |= 0x40;
                }
                if((sum >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(sum)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xBD: {
                flag = default_flag;
                if((A & 0x0F) < (L & 0x0F)) {
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~L) + 1;
                if(!(sum > 0xFF)){
                    flag |= 0x01;
                }
                sum &= 0xFF;
                if(sum == 0){
                    flag |= 0x40;
                }
                if((sum >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(sum)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xBE: {
                uint8_t M = memory[H<<8|L];
                flag = default_flag;
                if((A & 0x0F) < (M & 0x0F)) {
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~M) + 1;
                if(!(sum > 0xFF)){
                    flag |= 0x01;
                }
                sum &= 0xFF;
                if(sum == 0){
                    flag |= 0x40;
                }
                if((sum >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(sum)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xBF: {
                flag = default_flag;
                if((A & 0x0F) < (A & 0x0F)) {
                    flag |= 0x10;
                }                
                uint16_t sum = A + (~A) + 1;
                if(!(sum > 0xFF)){
                    flag |= 0x01;
                }
                sum &= 0xFF;
                if(sum == 0){
                    flag |= 0x40;
                }
                if((sum >> 7) & 1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(sum)%2)){
                    flag |= 0x04;
                }
                pc += 1;
                break;
            }
            case 0xC0: {
                if(!(flag&0x40)){
                    pc = (memory[sp+1] << 8)|memory[sp];
                    sp += 2;
                }
                else{
                    pc += 1;
                }
                break;
            }
            case 0xC1: {
                C = memory[sp];
                B = memory[sp + 1];
                sp += 2;
                pc += 1;
                break;
            }
            case 0xC2: {
                if(!(flag&0x40)){
                    pc = memory[pc+2]<<8|memory[pc+1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xC3: {
                pc = memory[pc+2]<<8|memory[pc+1];
                break;
            }
            case 0xC4: {
                if(!(flag&0x40)){
                    uint16_t temp_pc = pc + 3;
                    sp -= 2;
                    memory[sp] = temp_pc & 0xFF;
                    memory[sp + 1] = (temp_pc >> 8) & 0xFF;
                    pc = (memory[pc + 2] << 8)| memory[pc + 1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xC5: {
                sp -= 2;
                memory[sp] = C;
                memory[sp + 1] = B;
                pc += 1;
                break;
            }
            case 0xC6: {
                uint8_t immediate_val = memory[pc + 1];
                flag = default_flag;
                if((A&0x0F) + (immediate_val&0x0F) > 0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A + memory[pc + 1];
                if(sum>0xFF){
                    flag |= 0x01;
                }
                A = sum & 0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                if((A>>7)&1){
                    flag |= 0x80;
                }
                pc += 2;
                break;
            }
            case 0xC7: {
                uint16_t temp_pc = pc + 1;
                sp -= 2;
                memory[sp] = temp_pc & 0xFF;
                memory[sp+1] = (temp_pc >> 8) & 0xFF;
                pc = 0x0000;
                break;
            }
            case 0xC8: {
                if(flag&0x40){
                    pc = (memory[sp+1] << 8)|memory[sp];
                    sp += 2;
                }
                else{
                    pc += 1;
                }
                break;
            }
            case 0xC9: {
                pc = (memory[sp+1] << 8)|memory[sp];
                sp += 2;
                break;
            }
            case 0xCA: {
                if(flag&0x40){
                    pc = memory[pc+2]<<8|memory[pc+1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xCB: {
                printf("0xCB");
                running = false;
                break;
            }
            case 0xCC: {
                if(flag&0x40){
                    uint16_t temp_pc = pc + 3;
                    sp -= 2;
                    memory[sp] = temp_pc & 0xFF;
                    memory[sp + 1] = (temp_pc >> 8) & 0xFF;
                    pc = (memory[pc + 2] << 8)| memory[pc + 1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xCD: {
                uint16_t temp_pc = pc + 3;
                sp -= 2;
                memory[sp] = temp_pc & 0xFF;
                memory[sp + 1] = (temp_pc >> 8) & 0xFF;
                pc = (memory[pc + 2] << 8)| memory[pc + 1];
                break;
            }
            case 0xCE: {
                uint8_t immediate_val = memory[pc + 1];
                uint8_t carry = flag&0x01;
                flag = default_flag;
                if((A&0x0F) + carry + (immediate_val&0x0F) > 0x0F){
                    flag |= 0x10;
                }
                uint16_t sum = A + immediate_val + carry;
                if(sum > 0xFF){
                    flag |= 0x01;
                }
                A = sum&0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                if((A>>7)&1){
                    flag |= 0x80;
                }
                pc += 2;
                break;
            }
            case 0xCF: {
                uint16_t temp_pc = pc + 1;
                sp -= 2;
                memory[sp] = temp_pc & 0xFF;
                memory[sp+1] = (temp_pc >> 8) & 0xFF;
                pc = 0x0008;
                break;
            }
            case 0xD0: {
                if(!(flag&0x01)){
                    pc = (memory[sp+1] << 8)|memory[sp];
                    sp += 2;
                }
                else{
                    pc += 1;
                }
                break;
            }
            case 0xD1: {
                E = memory[sp];
                D = memory[sp + 1];
                sp += 2;
                pc += 1;
                break;
            }
            case 0xD2: {
                if(!(flag&0x01)){
                    pc = memory[pc+2]<<8|memory[pc+1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xD3: {
                uint8_t port = memory[pc + 1];
                out_port(port, A);
                pc += 2;
                break;
            }
            case 0xD4: {
                if(!(flag&0x01)){
                    uint16_t temp_pc = pc + 3;
                    sp -= 2;
                    memory[sp] = temp_pc & 0xFF;
                    memory[sp + 1] = (temp_pc >> 8) & 0xFF;
                    pc = (memory[pc + 2] << 8)| memory[pc + 1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xD5: {
                sp -= 2;
                memory[sp] = E;
                memory[sp + 1] = D;
                pc += 1;
                break;
            }
            case 0xD6: {
                uint8_t immediate_val = memory[pc + 1];
                flag = default_flag;
                if((A&0x0F) < (immediate_val&0x0F)){
                    flag |= 0x10;
                }
                uint16_t sum = A + (~immediate_val) + 1;
                if(A < immediate_val){
                    flag |= 0x01;
                }             
                A = sum&0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                if((A>>7)&1){
                    flag |= 0x80;
                }
                pc += 2;
                break;
            }
            case 0xD7: {
                uint16_t temp_pc = pc + 1;
                sp -= 2;
                memory[sp] = temp_pc & 0xFF;
                memory[sp+1] = (temp_pc >> 8) & 0xFF;
                pc = 0x0010;
                break;
            }
            case 0xD8: {
                if(flag&0x01){
                    pc = (memory[sp+1] << 8)|memory[sp];
                    sp += 2;
                }
                else{
                    pc += 1;
                }
                break;
            }
            case 0xD9: {
                printf("0xD9");
                running = false;
                break;
            }
            case 0xDA: {
                if(flag&0x01){
                    pc = memory[pc+2]<<8|memory[pc+1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xDB: {  // IN port
                uint8_t port = memory[pc + 1];
                A = in_port(port);  // You define this
                pc += 2;
                break;
            }
            case 0xDC: {
                if(flag&0x01){
                    uint16_t temp_pc = pc + 3;
                    sp -= 2;
                    memory[sp] = temp_pc & 0xFF;
                    memory[sp + 1] = (temp_pc >> 8) & 0xFF;
                    pc = (memory[pc + 2] << 8)| memory[pc + 1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xDD: {
                printf("0xDD");
                running = false;
                break;
            }
            case 0xDE: {
                uint8_t carry = flag & 0x01;
                uint8_t immediate_val = memory[pc + 1];
                flag = default_flag;
                if((A&0x0F) < ((immediate_val + carry)&0x0F)){
                    flag |= 0x10;
                }
                uint16_t sum = A + (~(immediate_val + carry)) + 1;
                if(A < (immediate_val + carry)){
                    flag |= 0x01;
                }
                A = sum&0xFF;
                if(A == 0){
                    flag |= 0x40;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                if((A>>7)&1){
                    flag |= 0x80;
                }
                pc += 2;
                break;
            }
            case 0xDF: {
                uint16_t temp_pc = pc + 1;
                sp -= 2;
                memory[sp] = temp_pc & 0xFF;
                memory[sp+1] = (temp_pc >> 8) & 0xFF;
                pc = 0x0018;
                break;
            }
            case 0xE0: {
                if(!(flag&0x04)){
                    pc = (memory[sp+1] << 8)|memory[sp];
                    sp += 2;
                }
                else{
                    pc += 1;
                }
                break;
            }
            case 0xE1: {
                L = memory[sp];
                H = memory[sp + 1];
                sp += 2;
                pc += 1;
                break;
            }
            case 0xE2: {
                if(!(flag&0x04)){
                    pc = memory[pc+2]<<8|memory[pc+1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xE3: {
                uint8_t temp_H = H, temp_L = L;
                H = memory[sp];
                L = memory[sp + 1];
                memory[sp] = temp_H;
                memory[sp + 1] = temp_L;
                pc += 1;
                break;
            }
            case 0xE4: {
                if(!(flag&0x04)){
                    uint16_t temp_pc = pc + 3;
                    sp -= 2;
                    memory[sp] = temp_pc & 0xFF;
                    memory[sp + 1] = (temp_pc >> 8) & 0xFF;
                    pc = (memory[pc + 2] << 8)| memory[pc + 1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xE5: {
                sp -= 2;
                memory[sp] = L;
                memory[sp + 1] = H;
                pc += 1;
                break;
            }
            case 0xE6: {
                flag = default_flag;
                uint8_t immediate_val = memory[pc + 1];
                A &= immediate_val;
                if(A == 0){
                    flag |= 0x40;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                if((A>>7)&1){
                    flag |= 0x80;
                }
                pc += 2;
                break;
            }
            case 0xE7: {
                uint16_t temp_pc = pc + 1;
                sp -= 2;
                memory[sp] = temp_pc & 0xFF;
                memory[sp+1] = (temp_pc >> 8) & 0xFF;
                pc = 0x0020;
                break;
            }
            case 0xE8: {
                if(flag&0x04){
                    pc = (memory[sp+1] << 8)|memory[sp];
                    sp += 2;
                }
                else{
                    pc += 1;
                }
                break;
            }
            case 0xE9: {
                pc = (H<<8)|L;
                break;
            }
            case 0xEA: {
                if(flag&0x04){
                    pc = memory[pc+2]<<8|memory[pc+1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xEB: {
                uint8_t temp_H = H, temp_L = L;
                H = D;
                L = E;
                D = temp_H;
                E = temp_L;
                pc += 1;
                break;
            }
            case 0xEC: {
                if(flag&0x04){
                    uint16_t temp_pc = pc + 3;
                    sp -= 2;
                    memory[sp] = temp_pc & 0xFF;
                    memory[sp + 1] = (temp_pc >> 8) & 0xFF;
                    pc = (memory[pc + 2] << 8)| memory[pc + 1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xED: {
                printf("0xED");
                running = false;
                break;
            }
            case 0xEE: {
                flag = default_flag;
                A ^= memory[pc + 1];
                if(A == 0){
                    flag |= 0x40;
                }
                if((A>>7)&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 2;
                break;
            }
            case 0xEF: {
                uint16_t temp_pc = pc + 1;
                sp -= 2;
                memory[sp] = temp_pc & 0xFF;
                memory[sp+1] = (temp_pc >> 8) & 0xFF;
                pc = 0x0028;
                break;
            }
            case 0xF0: {
                if(!(flag&0x80)){
                    pc = (memory[sp+1] << 8)|memory[sp];
                    sp += 2;
                }
                else{
                    pc += 1;
                }
                break;
            }
            case 0xF1: {
                flag = memory[sp];
                A = memory[sp + 1];
                sp += 2;
                pc += 1;
                break;
            }
            case 0xF2: {
                if(!(flag&0x80)){
                    pc = memory[pc+2]<<8|memory[pc+1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xF3: {
                interrupt_enabled = false;
                pc += 1;
                break;
            }
            case 0xF4: {
                if(!(flag&0x80)){
                    uint16_t temp_pc = pc + 3;
                    sp -= 2;
                    memory[sp] = temp_pc & 0xFF;
                    memory[sp + 1] = (temp_pc >> 8) & 0xFF;
                    pc = (memory[pc + 2] << 8)| memory[pc + 1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xF5: {
                sp -= 2;
                memory[sp] = flag;
                memory[sp + 1] = A;
                pc += 1;
                break;
            }
            case 0xF6: {
                flag = default_flag;
                A |= memory[pc + 1];
                if(A == 0){
                    flag |= 0x40;
                }
                if((A>>7)&1){
                    flag |= 0x80;
                }
                if(!(__builtin_popcount(A)%2)){
                    flag |= 0x04;
                }
                pc += 2;
                break;
            }
            case 0xF7: {
                uint16_t temp_pc = pc + 1;
                sp -= 2;
                memory[sp] = temp_pc & 0xFF;
                memory[sp+1] = (temp_pc >> 8) & 0xFF;
                pc = 0x0030;
                break;
            }
            case 0xF8: {
                if(flag&0x80){
                    pc = (memory[sp+1] << 8)|memory[sp];
                    sp += 2;
                }
                else{
                    pc += 1;
                }
                break;
            }
            case 0xF9: {
                sp = (H<<8)|L;
                pc += 1;
                break;
            }
            case 0xFA: {
                if(flag&0x80){
                    pc = memory[pc+2]<<8|memory[pc+1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xFB: {
                interrupt_enabled = true;
                pc += 1;
                break;
            }
            case 0xFC: {
                if(flag&0x80){
                    uint16_t temp_pc = pc + 3;
                    sp -= 2;
                    memory[sp] = temp_pc & 0xFF;
                    memory[sp + 1] = (temp_pc >> 8) & 0xFF;
                    pc = (memory[pc + 2] << 8)| memory[pc + 1];
                }
                else{
                    pc += 3;
                }
                break;
            }
            case 0xFD: {
                printf("0xFD");
                running = false;
                break;
            }
            case 0xFE: {
                uint8_t immediate_val = memory[pc + 1];
                flag = default_flag;
                if((A&0x0F) < (immediate_val&0x0F)){
                    flag |= 0x10;
                }
                uint16_t sum = A + (~immediate_val) + 1;
                if(A < immediate_val){
                    flag |= 0x01;
                }
                sum &= 0xFF;
                if(sum == 0){
                    flag |= 0x40;
                }
                if(!(__builtin_popcount(sum)%2)){
                    flag |= 0x04;
                }
                if((sum>>7)&1){
                    flag |= 0x80;
                }
                pc += 2;
                break;
            }
            case 0xFF: {
                uint16_t temp_pc = pc + 1;
                sp -= 2;
                memory[sp] = temp_pc & 0xFF;
                memory[sp+1] = (temp_pc >> 8) & 0xFF;
                pc = 0x0038;
                break;
            }
        }
    }
    return 0;
}
