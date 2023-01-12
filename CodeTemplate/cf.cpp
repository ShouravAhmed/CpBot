#include <bits/stdc++.h>

#include <ext/pb_ds/tree_policy.hpp>
#include <ext/pb_ds/assoc_container.hpp>

using namespace std;
using namespace __gnu_pbds;

#pragma GCC optimize("Ofast,no-stack-protector")
#pragma GCC target("sse,sse2,sse3,ssse3,sse4,popcnt,abm,mmx,avx,tune=native")
#pragma GCC optimize("unroll-loops")

//************** ah_med *********************

#define ll                  long long int
#define ull                 unsigned long long
#define ld                  long double
#define lll                 __int128
#define vi                  vector<int>
#define vvi                 vector<vector<int> >
#define pii                 pair<int,int>
#define piii                pair<int,pair<int,int> >

#define all(s)              s.begin(),s.end()
#define allr(s)             s.rbegin(),s.rend()
#define sz(v)               ((int)(v).size())
#define pb                  push_back
#define pob                 pop_back
#define ff                  first
#define ss                  second
#define sc                  scanf
#define pf                  printf

#define MS0(v)              memset((v), 0, sizeof((v)))
#define MS1(v)              memset((v), -1, sizeof((v)))

#define gcd(a, b)           __gcd(a, b)
#define lcm(a, b)           ((a)*((b)/gcd(a,b)))

#define unq(c)              (sort(all(c)), c.resize(distance(c.begin(),unique(all(c)))))
#define min_ele(v)          (*min_element(all(v)))
#define max_ele(v)          (*max_element(all(v)))
#define get_pos(c,x)        (lower_bound(all(c),x)-c.begin())

#define is_equal(x, y)      (abs(x-y)<eps)
#define cnt_ele(v, x)       (count(all(v), x))
#define sum_ele(v)          (accumulate(all(v),0))
#define pro_ele(v)          (accumulate(all(v),1, multiplies<int>()))
#define init_range(v, x)    (iota(all(v),x))

#define min_pq              priority_queue<int,vector<int>,greater<int> >
template <typename T>  	    using ordered_set = tree<T, null_type, less<T>, rb_tree_tag, tree_order_statistics_node_update>;

inline int random(int _min, int _max)   { static bool first = true; if (first)  {  srand(time(NULL)); first = false; } return _min + rand() % (( _max + 1 ) - _min); }
#define shuffle(v)                      (random_shuffle(all(v)))

#define vpf(v)              for(int _i=0;_i<v.size();_i++) cout<< v[_i] << " \n"[_i == v.size()-1];
#define vsc(v)              for(int _i=0;_i<v.size();_i++) cin >> v[_i];

#define FOR(i, n)           for(int i = 0; i < n; i++)
#define ROF(i, n)           for(int i = n-1; i >= 0; i--)

#define intmx               INT_MAX
#define inf                 1llu<<61
#define PI                  3.14159265358979323846264338327950L
#define MOD                 1000000007

inline ll  exp(ll a, ll b)          { a %= MOD; ll res = 1; while (b > 0) { if(b & 1) { res = res * a % MOD; } a = a * a % MOD; b >>= 1; } return res; }
inline int add(int a, int b)        { a += b; if(a >= MOD) a -= MOD; return a; }
inline int sub(int a, int b)        { a -= b; if(a < 0) a += MOD; return a; }
inline int multi(ll a, ll b)        { a *= b; if(a >= MOD) a %= MOD; return a; }

inline int on_bit(int N,int pos)    {return N = N | (1<<pos);}
inline int off_bit(int N,int pos)   {return N = N & ~(1<<pos);}
inline bool check_bit(ll N,int pos) {return (bool)(N & (1<<pos));}
#define on_bit_cnt(x)               (__builtin_popcount(x))
#define on_bit_cntll(x)             (__builtin_popcountll(x))
#define lsb(x)                      (__builtin_ffsll(x)-1)

#define TEST_CASE                   int ___T; cin>>___T; for(int cs=1;cs<=___T;cs++)
#define PRINT_CASE                  cout << "Case " << cs << ": ";
#define PRINT_CASEN                 cout << "Case " << cs << ":\n";
template<class T>                   inline bool read(T &x) {int c=getchar();int sgn=1;while(~c&&c<'0'||c>'9'){if(c=='-')sgn=-1;c=getchar();}for(x=0;~c&&'0'<=c&&c<='9';c=getchar())x=x*10+c-'0'; x*=sgn; return ~c;}

#define fastio                      ios_base::sync_with_stdio(0);cin.tie(0);cout.tie(0)

// debuger ------------------------------------------
#ifndef ONLINE_JUDGE
    #define debug(...) __f(#__VA_ARGS__, __VA_ARGS__)
    template < typename Arg1 >
    void __f(const char* name, Arg1&& arg1){
        cout << name << " = " << arg1 << std::endl;
    }
    template < typename Arg1, typename... Args>
    void __f(const char* names, Arg1&& arg1, Args&&... args){
        const char* comma = strchr(names, ',');
        cout.write(names, comma - names) << " = " << arg1 <<" | ";
        __f(comma+1, args...);
    }

    clock_t tStart;
    #define start_clock     tStart = clock()
    #define end_clock       printf("\n>>Runtime: %.10fs\n", (double) (clock() - tStart) / CLOCKS_PER_SEC)

    #define filein          freopen("in","r",stdin)
    #define fileout         freopen("out","w",stdout)

#else
    #define debug(...)      {int skip;}

    #define start_clock     {int skip;}
    #define end_clock       {int skip;}

    #define filein          {int skip;}
    #define fileout         {int skip;}
#endif
// --------------------------------------------------

#define eps             1e-9
#define MAX             100010

// lambda: auto f = [] (int a, int b) -> int { return a + b; };

// cartesian move
// int dr[] = {-1, 0, 1, 0};
// int dc[] = { 0, 1, 0,-1};

// king's move
// int dr[] = {-1,-1,-1, 0, 1, 1, 1, 0};
// int dc[] = {-1, 0, 1, 1, 1, 0,-1,-1};

// knight's move
// int dr[] = { 1, 2, 2, 1,-1,-2,-2,-1};
// int dc[] = { 2, 1,-1,-2,-2,-1, 1, 2};

//******************* my code starts here **********************************



int main() {

    filein;
    fileout;

    

    return 0;
}