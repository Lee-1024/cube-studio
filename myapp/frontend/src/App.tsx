import React, { useEffect, useState } from 'react';
import {
  BrowserRouter as Routers,
  useRoutes,
  useNavigate,
  useLocation,
  RouteObject
} from "react-router-dom";

import { Drawer, Dropdown, Menu, Select, Spin, Tag } from 'antd';
import { IRouterConfigPlusItem } from './api/interface/baseInterface';
import { formatRoute, getDefaultOpenKeys, routerConfigPlus } from './routerConfig';
import SubMenu from 'antd/lib/menu/SubMenu';
import { clearWaterNow, drawWater, drawWaterNow, getParam, obj2UrlParam, parseParam2Obj } from './util'
import { getAppHeaderConfig, getAppMenu, getCustomDialog, userLogout } from './api/kubeflowApi';
import { IAppHeaderItem, IAppMenuItem, ICustomDialog } from './api/interface/kubeflowInterface';
import { AlignRightOutlined, AppstoreOutlined, DownOutlined, GithubOutlined, LeftOutlined, QuestionCircleOutlined, RightOutlined, SlidersOutlined } from '@ant-design/icons';
import Cookies from 'js-cookie'
import { changeTheme } from './theme';
import { handleTips } from './api';
const userName = Cookies.get('myapp_username')

const RouterConfig = (config: RouteObject[]) => {
  let element = useRoutes(config);
  return element;
}

const getRouterMap = (routerList: IRouterConfigPlusItem[]): Record<string, IRouterConfigPlusItem> => {
  const res: Record<string, IRouterConfigPlusItem> = {}
  const queue = [...routerList]
  while (queue.length) {
    const item = queue.shift()
    if (item) {
      res[item?.path || ''] = item
      if (item?.children && item.children.length) {
        queue.push(...item.children)
      }
    }
  }
  return res
}

const getValidAppList = (config: IRouterConfigPlusItem[]) => config.filter(item => !!item.name && !item.hidden)

interface IProps { }

const AppWrapper = (props: IProps) => {
  const [openKeys, setOpenKeys] = useState<string[]>([])
  const [currentNavList, setCurrentNavList] = useState<IRouterConfigPlusItem[]>([])
  const [sourceAppList, setSourceAppList] = useState<IRouterConfigPlusItem[]>([])
  const [sourceAppMap, setSourceAppMap] = useState<Record<string, IRouterConfigPlusItem>>({})
  const [CurrentRouteComponent, setCurrentRouteComponent] = useState<any>()
  const [isMenuCollapsed, setIsMenuCollapsed] = useState(false)
  const [isShowSlideMenu, setIsShowSlideMenu] = useState(true)
  const [imgUrlProtraits, setImgUrlProtraits] = useState('')
  const [customDialogVisable, setCustomDialogVisable] = useState(false)
  const [customDialogInfo, setCustomDialogInfo] = useState<ICustomDialog>()
  const [headerConfig, setHeaderConfig] = useState<IAppHeaderItem[]>([])
  const [navSelected, setNavSelected] = useState<string[]>([])
  const isShowNav = getParam('isShowNav')

  const navigate = useNavigate();
  const location = useLocation()

  useEffect(() => {
    getAppMenu().then(res => {
      const remoteRoute = res.data
      const dynamicRoute = formatRoute([...remoteRoute])
      const tarRoute = [...dynamicRoute, ...routerConfigPlus]
      const tarRouteMap = getRouterMap(tarRoute)

      setSourceAppList(tarRoute)
      setSourceAppMap(tarRouteMap)

      const defaultOpenKeys = getDefaultOpenKeys(tarRoute)
      setOpenKeys(defaultOpenKeys)

      setCurrentRouteComponent(() => () => RouterConfig(tarRoute as RouteObject[]))
    }).catch(err => { })

    getAppHeaderConfig().then(res => {
      const config = res.data
      setHeaderConfig(config)
    }).catch(err => { })
  }, [])

  useEffect(() => {
    if (sourceAppList.length && Object.keys(sourceAppMap).length) {
      const { pathname } = location
      if (pathname === '/') {
        clearWaterNow()
      } else {
        drawWaterNow()
      }
      handleCurrentRoute(sourceAppMap, getValidAppList(sourceAppList))
      handleChangePageTitle(pathname, sourceAppList)
    }
  }, [location, sourceAppList, sourceAppMap])

  useEffect(() => {
    const url = encodeURIComponent(location.pathname)
    getCustomDialog(url).then(res => {
      setCustomDialogInfo(res.data)
      setCustomDialogVisable(res.data.hit)
    }).catch(err => {
      console.log(err);
    })
  }, [location])

  const handleCurrentRoute = (appMap: Record<string, IRouterConfigPlusItem>, appList: IRouterConfigPlusItem[]) => {
    const { pathname } = location
    const [_, stLevel, edLevel] = pathname.split('/')
    const currentApp = appMap[pathname]
    const stLevelApp = appMap[`/${stLevel}`]
    let currentNavKey = ""
    if (stLevelApp && stLevelApp.isSingleModule) {
      currentNavKey = `/${stLevel}/${edLevel}`
    } else {
      currentNavKey = `/${stLevel}`
    }

    console.log('stLevelApp', stLevelApp);

    let topNavAppList = appList
    if (stLevelApp && stLevelApp.isSingleModule) {
      topNavAppList = stLevelApp.children || []
    }

    setCurrentNavList(topNavAppList)
    setNavSelected([currentNavKey])
    setIsShowSlideMenu(stLevelApp && !stLevelApp.isCollapsed)
  }

  const handleClickNav = (app: IRouterConfigPlusItem, subPath?: string) => {
    console.log('app', app)
    if (app.path === '/') {
      commitUrlChange('/')
      navigate(app.path || '/')
    } else if (app.menu_type === 'iframe' && app.path) {
      commitUrlChange(app.path)
      navigate(app.path)
    } else if (app.menu_type === 'out_link' && app.url) {
      window.open(app.url, 'blank')
    } else if (app.menu_type === 'in_link' && app.path) {
      window.open(app.url, 'blank')
    } else {
      const currentApp = sourceAppMap[subPath || '']
      let currentItem = subPath ? currentApp : app

      while (currentItem && currentItem.children) {
        currentItem = currentItem.children[0]
      }

      if (currentItem) {
        let appMenuPath = currentItem.path || ''
        commitUrlChange(appMenuPath)
        navigate(appMenuPath)
      }
    }
  }

  const handleChangePageTitle = (pathname: string, currnetRouteConfig: IRouterConfigPlusItem[]) => {
    const currentAppName = '/' + pathname.substring(1).split('/')[0] || ''
    const routerMap: Record<string, IRouterConfigPlusItem> = currnetRouteConfig.reduce((pre: any, next) => ({ ...pre, [`${next.path || ''}`]: next }), {})
    const currentRoute = routerMap[currentAppName]
    if (currentRoute && currentRoute.title) {
      document.title = `星云 - ${currentRoute.title}`
    } else {
      document.title = '星云数据平台'
    }
  }

  const commitUrlChange = (key: string) => {
    if (window !== window.top) {
      const locationTop = (window as any).top.location
      const href = locationTop.href
      const path = locationTop.origin + locationTop.pathname
      const search = href.split('?').slice(1).join('?')
      const paramObj = parseParam2Obj(search)
      paramObj['pathUrl'] = key;
      const paramStr = obj2UrlParam(paramObj);
      const currentUrl = path + '#/?' + paramStr;

      (window as any).top.location.href = currentUrl
    }
  }

  const renderMenu = () => {
    const { pathname } = location
    const currentNavMap = sourceAppMap
    const [currentSelected] = navSelected

    if (currentNavMap && currentSelected && currentNavMap[currentSelected]?.children?.length) {

      const currentAppMenu = currentNavMap[currentSelected].children
      if (currentAppMenu && currentAppMenu.length) {

        const menuContent = currentAppMenu.map(menu => {
          if (menu.isMenu) {
            return <SubMenu key={menu.path} title={menu.title}>
              {
                menu.children?.map(sub => {
                  if (sub.isMenu) {
                    return <Menu.ItemGroup key={sub.path} title={sub.title}>
                      {
                        sub.children?.map(thr => {
                          return <Menu.Item disabled={!!thr.disable} hidden={!!thr.hidden} key={thr.path} onClick={() => {
                            if (!menu.isCollapsed) {
                              setIsMenuCollapsed(false)
                            }
                            if (thr.menu_type === 'out_link' || thr.menu_type === 'in_link') {
                              window.open(thr.url, 'blank')
                            } else {
                              navigate(thr.path || '')
                            }
                          }}>
                            <div className="icon-wrapper">
                              {
                                Object.prototype.toString.call(thr.icon) === '[object String]' ? <div className="icon-custom svg16 mr8" dangerouslySetInnerHTML={{ __html: thr.icon }}></div> : sub.icon
                              }
                              {/* <div className="icon-custom svg16 mr8" dangerouslySetInnerHTML={{ __html: thr.icon }}></div> */}
                              {thr.title}
                            </div>
                          </Menu.Item>
                        })
                      }
                    </Menu.ItemGroup>
                  }
                  return <Menu.Item disabled={!!sub.disable} hidden={!!sub.hidden} key={sub.path} onClick={() => {
                    if (!menu.isCollapsed) {
                      setIsMenuCollapsed(false)
                    }
                    if (sub.menu_type === 'out_link' || sub.menu_type === 'in_link') {
                      window.open(sub.url, 'blank')
                    } else {
                      navigate(sub.path || '')
                    }
                  }}>
                    <div className="icon-wrapper">
                      {
                        Object.prototype.toString.call(sub.icon) === '[object String]' ? <div className="icon-custom svg16 mr8" dangerouslySetInnerHTML={{ __html: sub.icon }}></div> : sub.icon
                      }
                      {sub.title}
                    </div>
                  </Menu.Item>
                })
              }
            </SubMenu>
          }
          return <Menu.Item disabled={!!menu.disable} hidden={!!menu.hidden} key={menu.path} onClick={() => {
            if (!menu.isCollapsed) {
              setIsMenuCollapsed(false)
            }
            if (menu.menu_type === 'out_link' || menu.menu_type === 'in_link') {
              window.open(menu.url, 'blank')
            } else {
              navigate(menu.path || '')
            }
          }}>
            <div className="icon-wrapper">
              {
                Object.prototype.toString.call(menu.icon) === '[object String]' ? <div className="icon-custom svg16 mr8" dangerouslySetInnerHTML={{ __html: menu.icon }}></div> : menu.icon
              }
              {menu.title}
            </div>
          </Menu.Item>
        })

        return <div className="side-menu">
          <div className="h100 ov-h d-f fd-c" style={{ width: isMenuCollapsed ? 0 : 'auto' }}>
            <Menu
              selectedKeys={[pathname]}
              openKeys={openKeys}
              mode="inline"
              onOpenChange={(openKeys) => {
                setOpenKeys(openKeys)
              }}
              onSelect={(info) => {
                const key = info.key
                commitUrlChange(key)
              }}
            >
              {menuContent}
            </Menu>
            <div className="p16 ta-r bor-t" style={{ borderColor: '#e5e6eb' }}>
              <div className="d-il bor-l pl16" style={isMenuCollapsed ? { position: 'absolute', bottom: 16, left: 0, borderColor: '#e5e6eb' } : { borderColor: '#e5e6eb' }}>
                {
                  isMenuCollapsed ? <RightOutlined className="cp" onClick={() => {
                    setIsMenuCollapsed(!isMenuCollapsed)
                  }} /> : <LeftOutlined className="cp" onClick={() => {
                    setIsMenuCollapsed(!isMenuCollapsed)
                  }} />
                }
              </div>
            </div>
          </div>

          {/* <div className="menu-collapsed cp">
            <span className="w100 h100 d-f jc ac p-a" onClick={() => {
              setIsMenuCollapsed(!isMenuCollapsed)
            }}>{
                isMenuCollapsed ? <RightOutlined style={{ color: '#d9d9d9' }} /> : <LeftOutlined style={{ color: '#d9d9d9' }} />
              }</span>
            <img src={require('./images/sideLeft.png')} alt="" />
          </div> */}


        </div>
      }
    }

    return null
  }

  const renderNavTopMenu = () => {
    return currentNavList.map((app) => {
      if (!!app.hidden) {
        return null
      }
      if (app.isSingleModule || app.isDropdown) {
        return <Menu.SubMenu key={app.path} title={
          <div className="star-topnav-submenu" onClick={() => {
            if (app.isDropdown) {
              return
            }
            handleClickNav(app)
          }}>
            {
              Object.prototype.toString.call(app.icon) === '[object String]' ? <div className="icon-custom" dangerouslySetInnerHTML={{ __html: app.icon }}></div> : app.icon
            }
            <div className="mainapp-topmenu-name">{app.title}</div>
            <DownOutlined className="ml8" />
          </div>
        }>
          {
            (app.children || []).map(subapp => {
              return <Menu.Item key={subapp.path} onClick={() => {
                handleClickNav(subapp, subapp.path)
              }}>
                <div className="d-f ac">
                  {
                    Object.prototype.toString.call(subapp.icon) === '[object String]' ? <div className="icon-custom" dangerouslySetInnerHTML={{ __html: subapp.icon }}></div> : subapp.icon
                  }
                  <div className="pl8">{subapp.title}</div>
                </div>
              </Menu.Item>
            })
          }
        </Menu.SubMenu>
      }
      return <Menu.Item key={app.path} onClick={() => {
        handleClickNav(app)
      }}>
        {
          Object.prototype.toString.call(app.icon) === '[object String]' ? <div className="icon-custom" dangerouslySetInnerHTML={{ __html: app.icon }}></div> : app.icon
        }
        <div className="mainapp-topmenu-name">{app.title}</div>
      </Menu.Item>
    })
  }

  const renderSingleModule = () => {
    const { pathname } = location
    const [_, stLevel] = pathname.split('/')
    const stLevelApp = sourceAppMap[`/${stLevel}`]
    if (stLevelApp && stLevelApp.isSingleModule) {
      return <Tag color="#1672fa">{stLevelApp.title}</Tag>
    }
    return null
  }

  return (
    <div className="content-container fade-in">

      {/* Header */}
      {
        isShowNav === 'false' ? null : <div className="navbar">
          <div className="d-f ac pl48 h100">
            <div className="d-f ac">
              <div className="cp pr16" style={{ width: 'auto' }} onClick={() => {
                navigate('/', { replace: true })
              }}>
                <img style={{ height: 42 }} src={require("./images/logoCB.svg").default} alt="img" />
              </div>

              {
                renderSingleModule()
              }
            </div>
            <div className="star-topmenu">
              <Menu mode="horizontal" selectedKeys={navSelected}>
                {renderNavTopMenu()}
              </Menu>
            </div>
          </div>

          <div className="d-f ac plr16 h100">

            {/* <div className="mr16">
            <Select
              bordered={false}
              defaultValue="star"
              options={[
                { label: '无垠星空主题', value: 'star' },
                { label: '清新蓝调主题', value: 'blue' },
              ]}
              onChange={(value: any) => {
                changeTheme(value)
              }}
            />
          </div> */}

            {/* <a
              href="https://doc.weixin.qq.com/doc/w3_AGMAOAb-ACMUD0tIlQfR4u1BIj2nc?scode=AJEAIQdfAAoC8AWAeuAfoApAY1AC8"
              target="_blank"
              className="mr12 d-f ac"
            >
              <span className="pr4">平台文档</span><QuestionCircleOutlined style={{ fontSize: 20, color: "#1672fa" }} />
            </a>


            <GithubOutlined className="mr24" style={{ fontSize: 20, color: "#1672fa" }} onClick={() => {
              window.open('https://github.com/tencentmusic/cube-studio', '_bank')
            }} /> */}

            {
              headerConfig.map(config => {
                if (config.icon) {
                  return <a
                    href={config.link}
                    target="_blank"
                    className="mr12 d-f ac" rel="noreferrer"
                  >
                    <span className="pr4">{config.text}</span><span className="icon-custom" dangerouslySetInnerHTML={{ __html: config.icon }}></span>
                  </a>
                } else if (config.pic_url) {
                  return <a
                    href={config.link}
                    target="_blank"
                    className="mr12 d-f ac" rel="noreferrer"
                  >
                    <span className="pr4">{config.text}</span><img style={{ height: 30 }} src={config.pic_url} alt="" />
                  </a>
                }
              })
            }

            <Dropdown overlay={<Menu>
              <Menu.Item onClick={() => {
                navigate('/user')
              }}>用户中心</Menu.Item>
              <Menu.Item onClick={() => {
                Cookies.remove('myapp_username');
                handleTips.userlogout()
              }}>退出登录</Menu.Item>
            </Menu>
            }>
              <img className="mr8 cp" style={{ borderRadius: 200, height: 32 }} src={imgUrlProtraits} onError={() => {
                setImgUrlProtraits(require('./images/male.png'))
              }} alt="img" />
            </Dropdown>
          </div>
        </div>
      }


      {/* Document */}
      <div className="main-content-container">
        {/* <a
          href="https://github.com/tencentmusic/cube-studio/tree/master/docs/example"
          target="_blank"
          className="helpDoc"
        >
          平<br />台<br />文<br />档<br />
          <img src={require('./images/right.png')} />
        </a> */}

        {/* old side nav */}
        {/* {
          currentAppList.filter(app => !!app.hidden).length ? <ul className="mainapp-sidemenu">
            {
              currentAppList.filter(app => !!app.hidden).map((app) => {
                const currentAppName = '/' + currentRoute.substring(1).split('/')[0] || ''
                return <li
                  onClick={() => handleClickNav(app, app.appIndex || 0)}
                  key={`appList${app.appIndex}`}
                  style={
                    currentAppName === app.path ? { background: "#fcfcfc", color: '#1e1653' } : {}
                  }
                >
                  <div className="icon-custom" dangerouslySetInnerHTML={{ __html: app.icon }}></div>
                  <div className="mainapp-sidemenu-name">{app.title}</div>
                </li>
              })
            }
          </ul> : null
        } */}
        {isShowSlideMenu ? renderMenu() : null}

        <div className="ov-a w100 bg-title p-r" id="componentContainer">
          {/* 自定义弹窗 */}
          {
            customDialogVisable ? <Drawer
              getContainer={false}
              style={{ position: 'absolute', height: 'calc(100vh - 100px)', top: '10%', ...customDialogInfo?.style }}
              bodyStyle={{ padding: 0 }}
              mask={false}
              contentWrapperStyle={{ width: 'auto' }}
              title={customDialogInfo?.title} placement="right" onClose={() => { setCustomDialogVisable(false) }}
              visible={customDialogVisable}>
              <div className="h100" dangerouslySetInnerHTML={{ __html: customDialogInfo?.content || '' }}></div>
            </Drawer> : null
          }
          {
            CurrentRouteComponent && <CurrentRouteComponent />
          }
          {/* <div className="ta-c ptb16">©2023 by Data Leap All Rights Reserved</div> */}
        </div>

        {
          customDialogInfo?.content ? <div className="c-text-w fs12 p-f" style={{ backgroundColor: 'transparent', zIndex: 10, right: 16, bottom: 32 }}>
            <div className="bg-theme d-f jc ac cp" style={{ borderRadius: 6, width: 36, height: 36 }} onClick={() => {
              setCustomDialogVisable(true)
            }}><AppstoreOutlined style={{ color: '#fff', fontSize: 22 }} /></div>
          </div> : null
        }

      </div >
    </div>
  );
};

export default AppWrapper;
