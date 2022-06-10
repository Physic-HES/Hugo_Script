function [errorCode, UserData1, UserData2, UserData3, UserData4, UserData5, UserData6, UserData7, UserData8] = GatheringUserDatasGet(socketId)
%GatheringUserDatasGet :  Return UserDatas values
%
%	[errorCode, UserData1, UserData2, UserData3, UserData4, UserData5, UserData6, UserData7, UserData8] = GatheringUserDatasGet(socketId)
%
%	* Input parameters :
%		int32 socketId
%	* Output parameters :
%		int32 errorCode
%		doublePtr UserData1
%		doublePtr UserData2
%		doublePtr UserData3
%		doublePtr UserData4
%		doublePtr UserData5
%		doublePtr UserData6
%		doublePtr UserData7
%		doublePtr UserData8


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
UserData1 = 0;
UserData2 = 0;
UserData3 = 0;
UserData4 = 0;
UserData5 = 0;
UserData6 = 0;
UserData7 = 0;
UserData8 = 0;

% lib call
[errorCode, UserData1, UserData2, UserData3, UserData4, UserData5, UserData6, UserData7, UserData8] = calllib('XPS_Q8_drivers', 'GatheringUserDatasGet', socketId, UserData1, UserData2, UserData3, UserData4, UserData5, UserData6, UserData7, UserData8);
