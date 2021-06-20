def airfoilinterpolater(airfoil1,airfoil2,chord1,chord2,y1,y2,y,frontspar,rearspar):
    g = open("CSTs.dat", "r")
    lines = g.read().split(' ')
    CSTcoefs = list(np.float_(lines))
    res = 51
    upperskin1 = np.zeros(res)
    lowerskin1 = np.zeros(res)
    upperskin2 = np.zeros(res)
    lowerskin2 = np.zeros(res)
    upperskin1 = []
    lowerskin1 = []
    upperskin2 = []
    lowerskin2 = []
    # upperskin1 = np.zeros((res,2))
    # lowerskin1 = np.zeros((res,2))
    # upperskin2 = np.zeros((res,2))
    # lowerskin2 = np.zeros((res,2))
    x1 = np.zeros(res)
    xx = np.zeros(res)
    xx = []
    x2 = np.zeros(res)
    upperskin = []
    lowerskin = []
    #frontspar = lala[7,0]/100
    #rearspar = lala[8,0]/100
    dist = (rearspar-frontspar)/(res-1)
    ydist = y2 - y1
    ything = (y-y1)/ydist
    chord = (chord1 * (2 - ything * 2) + chord2 * 2 * ything) / 2
    if airfoil1 == 0:
        j = 0
    if airfoil2 == 2:
        j = 12
    else:
        j=0

    for i in range(res):
        x = frontspar+dist*i
        #x1[i] = x * chord1
        xx.append(x*chord)
        #x2[i] = x * chord2
        #[upperskin1[i], lowerskin1[i]] = (Airfoilcoordinates(CSTcoefs[0+j:6+j], CSTcoefs[6+j:12+j],x))#*int(chord1)
        #[upperskin2[i], lowerskin2[i]]= (Airfoilcoordinates(CSTcoefs[12+j:18+j], CSTcoefs[18+j:24+j],x))#*int(chord2)
        [up1, low1] = (Airfoilcoordinates(CSTcoefs[0 + j:6 + j], CSTcoefs[6 + j:12 + j], x))# * int(chord1)
        [up2, low2] = (Airfoilcoordinates(CSTcoefs[12 + j:18 + j], CSTcoefs[18 + j:24 + j],x))# * int(chord2)
        # upperskin1[i] = up1#,x
        # lowerskin1[i] = low1#,x
        # upperskin2[i] = up2#,x
        # lowerskin2[i] = low2#,x
        upperskin1.append(up1)  # ,x
        lowerskin1.append(low1) # ,x
        upperskin2.append(up2)  # ,x
        lowerskin2.append(low2)  # ,x
        upperint = (up1*chord1*(2-ything*2)+up2*chord2*2*ything)/2
        lowerint = (low1*chord1 * (2 - ything * 2) + low2*chord2 * 2 * ything) / 2
        upperskin.append(upperint)
        lowerskin.append(lowerint)
    #upperskin = (upperskin1*chord1*(2-ything*2)+upperskin2*chord2*2*ything)/2
    #lowerskin = (lowerskin1*chord1 * (2 - ything * 2) + lowerskin2*chord2 * 2 * ything) / 2
    #Upperskin = [upperskin,xx]
    #Lowerskin = [lowerskin,xx]
    # plt.plot(upperskin[:,1],upperskin[:,0],label='0')
    # plt.plot(lowerskin[:,1],lowerskin[:,0],label='00')
    # plt.plot(upperskin1[:,1]*chord1,upperskin1[:,0]*chord1,label='1')
    # plt.plot(lowerskin1[:,1]*chord1,lowerskin1[:,0]*chord1,label='11')
    # plt.plot(upperskin1[:,1]*chord2,upperskin2[:,0]*chord2,label='2')
    # plt.plot(lowerskin1[:,1]*chord2,lowerskin2[:,0]*chord2,label='22')
    # plt.legend()
    # plt.show()
    return upperskin,lowerskin,xx