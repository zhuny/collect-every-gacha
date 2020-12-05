## Problem Definition
* 여기서 다루고자 하는 확률문제는 어떠한 목표가 있고 목표를 달성하기 위해 어느 정도의 비용을 지불할 것인지에 집중합니다.
* 가장 간단한 형태의 문제로는 다음이 있습니다.
  * 동전의 앞면이 나오기 위해서는 동전을 몇번 던져야 할까?
  * 그런데, 만약 동전을 한번 던지기 위해서 돈을 지불하려면?

## Markov chain
* [Wikipedia](https://en.wikipedia.org/wiki/Markov_chain)
* 여기서는 Discrete-time에 대해 finite state space 에서 논의합니다.

### Define State space
* 한 시스템에서 나올 수 있는 State를 정의합니다.

### Define transition
* 모든 state마다, 어떤 확률로 어디로 가는지에 대해서 설정합니다.
  * 모든 state에서 시작하는 확률은 합쳐서 1이 되어야 합니다. 

### Define needs
* 처음 state와 최종 목적 state를 설정합니다.
