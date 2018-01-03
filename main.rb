require "sinatra/base"
require "sinatra/cookies"
require "json"

class DailyFright < Sinatra::Application

  @data = nil

  def initialize()
    super()
    @data = JSON.parse(File.open("./backend/films.json").read)
  end
  def getFilm(id)
    return @data[id]
  end

  def getRandomFilm()
    return @data.keys.sample
  end

  get "/" do
    show = false
    film = nil
    if cookies[:date]
      t = Date.parse(cookies[:date])
      n = Date.today
      if n > t
        puts "Need to allow new selection"
        show = true
      else
        puts "Already had todays selection"
        film = getFilm(cookies[:film])
      end
    else
      show = true
    end
    erb :index, :locals => {:show => show, :film => film}
  end

  get "/new" do
    f = getRandomFilm()
    response.set_cookie(:film, :value => f, :expires => Time.now + 3600*24*7)
    response.set_cookie(:date, :value => Date.today, :expires => Time.now + 3600*24*7)
    redirect "/"
  end

  run! if app_file == $0
end
